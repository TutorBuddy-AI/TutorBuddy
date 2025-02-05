from aiogram import types, md, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy import select, desc, text, delete, Row, RowMapping, func

from src.config import bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.utils.answer import AnswerRenderer
from src.utils.stciker.sticker_sender import StickerSender
from src.utils.user import UserService
from src.database.models import Setting, User
from src.database import session

dailymessages_router = Router(name=__name__)

async def get_or_refresh_user_settings(tg_id: str,
                                       update_morning: bool = None,
                                       update_daily: bool = None,
                                       update_evening: bool = None) -> Setting:
    """
    Получает или обновляет настройки уведомлений пользователя.

    Функция сначала пытается получить текущие настройки уведомлений пользователя на основе его tg_id. 
    Если пользовательские настройки не существуют, создается новая запись с настройками по умолчанию 
    (все уведомления включены). Если переданы параметры для обновления настроек, они будут изменены, 
    а запись будет сохранена в базе данных.

    Если после обновления все настройки становятся True, запись удаляется из базы данных, так как 
    считается, что пользователь вернулся к значениям по умолчанию. Если хотя бы одна настройка становится 
    False, запись сохраняется.
    """

    query = select(Setting).where(Setting.tg_id == tg_id)
    result = await session.execute(query)
    settings = result.scalars().first()

    if not settings:
        settings = Setting(
            tg_id=tg_id,
            subscription_good_morning=True,
            subscription_daily_plans=True,
            subscription_good_evening=True
        )
        session.add(settings)
        await session.commit() 

    settings_changed = False

    if update_morning is not None:
        settings.subscription_good_morning = update_morning
        settings_changed = True
    
    if update_daily is not None:
        settings.subscription_daily_plans = update_daily
        settings_changed = True
    
    if update_evening is not None:
        settings.subscription_good_evening = update_evening
        settings_changed = True

    if settings_changed:
#        if settings.subscription_good_morning and settings.subscription_daily_plans and settings.subscription_good_evening:
#            await session.delete(settings)
#        else:
#            session.add(settings)
        await session.commit() 

    return settings


def get_notification_settings_markup(settings: Setting) -> InlineKeyboardMarkup:
    good_morning_btn = InlineKeyboardButton(
        text=f"Good Morning with Quote {'✅' if settings.subscription_good_morning else '❌'}",
        callback_data="toggle_morning_quote"
    )
    daily_plans_btn = InlineKeyboardButton(
        text=f"Daily Plans {'✅' if settings.subscription_daily_plans else '❌'}",
        callback_data="toggle_daily_plan"
    )
    good_evening_btn = InlineKeyboardButton(
        text=f"Good Evening {'✅' if settings.subscription_good_evening else '❌'}",
        callback_data="toggle_evening_quote"
    )
    newsletter_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[AnswerRenderer.get_button_text_translation_standalone(for_user=True)], [good_morning_btn], [daily_plans_btn], [good_evening_btn]]
    )

    return newsletter_keyboard


@dailymessages_router.message(IsRegister(), Command("dailymessages"))
async def dailymessages_handler(message: types.Message, state: FSMContext):
    tg_id = str(message.chat.id)

    settings = await get_or_refresh_user_settings(tg_id)

    await bot.send_message(
        tg_id,
        text="You can turn off notifications for 'Good Morning with Quote', 'Daily Plans' and 'Good Evening'",
        parse_mode=ParseMode.HTML,
        reply_markup=get_notification_settings_markup(settings)
    )


@dailymessages_router.callback_query(F.data == "toggle_morning_quote")
async def toggle_morning_quote_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id)  
    settings = await get_or_refresh_user_settings(tg_id, update_morning=not settings.subscription_good_morning)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))

@dailymessages_router.callback_query(F.data == "toggle_daily_plan")
async def toggle_daily_plan_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id) 
    settings = await get_or_refresh_user_settings(tg_id, update_daily=not settings.subscription_daily_plans)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))

@dailymessages_router.callback_query(F.data == "toggle_evening_quote")
async def toggle_evening_quote_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id)
    settings = await get_or_refresh_user_settings(tg_id, update_evening=not settings.subscription_good_evening)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))


@dailymessages_router.callback_query(F.data == "daily_question_ok")
async def daily_question_ok_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    query = select(Setting).where(Setting.tg_id == tg_id)
    result = await session.execute(query)
    settings = result.scalars().first()

    if not settings:
        settings = Setting(
            tg_id=tg_id,
            subscription_good_morning=True,
            subscription_daily_plans=True,
            subscription_good_evening=True,
            subscription_sent_counter = 0
        )
        session.add(settings)
        await session.commit()
    else:
        settings.subscription_good_morning=True
        settings.subscription_daily_plans=True
        settings.subscription_good_evening=True
        settings.subscription_sent_counter = 0
        await session.commit()

    user_info = await UserService().get_user_info(str(callback_query.from_user.id))
    sticker_sender = StickerSender(bot, callback_query.from_user.id, speaker=user_info["speaker"])
    await sticker_sender.send_yas_sticker()
    await bot.send_message(callback_query.from_user.id, text=f"Буду с тобой общаться, чтобы мы еще лучше сдружились,"
        " а ты улучшил свой разговорный английский 👏",
        parse_mode=ParseMode.HTML)

@dailymessages_router.callback_query(F.data == "daily_question_nope")
async def daily_question_ok_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    query = select(Setting).where(Setting.tg_id == tg_id)
    result = await session.execute(query)
    settings = result.scalars().first()

    if not settings:
        settings = Setting(
            tg_id=tg_id,
            subscription_good_morning=False,
            subscription_daily_plans=False,
            subscription_good_evening=False,
            subscription_sent_counter = 0
        )
        session.add(settings)
        await session.commit()
    else:
        settings.subscription_good_morning=False
        settings.subscription_daily_plans=False
        settings.subscription_good_evening=False
        settings.subscription_sent_counter = 0
        await session.commit()

    user_info = await UserService().get_user_info(str(callback_query.from_user.id))
    sticker_sender = StickerSender(bot, callback_query.from_user.id, speaker=user_info["speaker"])
    await sticker_sender.send_miss_you_sticker()
    text_a = "а"
    if user_info["speaker"] == 'TutorBuddy':
        text_a = ""
    await bot.send_message(callback_query.from_user.id,
        text=f"Жаль, я думал{text_a} буду заряжать тебя с самого утра и дальше обсуждать с тобой планы (\n"
        "Если ты нажал случайно или передумаешь - зайди в меню: /dailymessages 📝Daily messages",
        parse_mode=ParseMode.HTML)


@dailymessages_router.message(IsNotRegister(), Command("subscriptions"))
async def dailymessages_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text="Please, register first", parse_mode=ParseMode.HTML,
                           reply_markup=translate_markup)
