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
from src.database.models import Setting, User
from src.database import session

newsletter_router = Router(name=__name__)


async def get_or_refresh_user_settings(tg_id: str,
                                       update_morning: bool = None,
                                       update_daily: bool = None,
                                       update_evening: bool = None) -> Setting:
    query = select(Setting).where(Setting.tg_id == tg_id)
    result = await session.execute(query)
    settings = result.scalars().first()

    if update_morning is not None:
        settings.newsletter_good_morning = update_morning

    if update_daily is not None:
        settings.newsletter_daily_plans = update_daily

    if update_evening is not None:
        settings.newsletter_good_evening = update_evening

    if any([update_morning is not None, update_daily is not None, update_evening is not None]):
        await session.commit()

    return settings


def get_notification_settings_markup(settings: Setting) -> InlineKeyboardMarkup:
    good_morning_btn = InlineKeyboardButton(
        text=f"Good Morning with Quote {'✅' if settings.newsletter_good_morning else '❌'}",
        callback_data="toggle_morning_quote"
    )
    daily_plans_btn = InlineKeyboardButton(
        text=f"Daily Plans {'✅' if settings.newsletter_daily_plans else '❌'}",
        callback_data="toggle_daily_plan"
    )
    good_evening_btn = InlineKeyboardButton(
        text=f"Good Evening {'✅' if settings.newsletter_good_evening else '❌'}",
        callback_data="toggle_evening_quote"
    )
    newsletter_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[good_morning_btn], [daily_plans_btn], [good_evening_btn]]
    )

    return newsletter_keyboard


@newsletter_router.message(IsRegister(), Command("newsletter"))
async def newsletter_handler(message: types.Message, state: FSMContext):
    tg_id = str(message.chat.id)
    settings = await get_or_refresh_user_settings(tg_id)

    await bot.send_message(
        tg_id,
        text="You can turn off notifications for 'Good Morning with Quote', 'Daily Plans', and 'Good Evening",
        parse_mode=ParseMode.HTML,
        reply_markup=get_notification_settings_markup(settings)
    )


@newsletter_router.callback_query(F.data == "toggle_morning_quote")
async def toggle_morning_quote_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id)
    settings = await get_or_refresh_user_settings(tg_id, update_morning=not settings.newsletter_good_morning)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))


@newsletter_router.callback_query(F.data == "toggle_daily_plan")
async def toggle_daily_plan_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id)
    settings = await get_or_refresh_user_settings(tg_id, update_daily=not settings.newsletter_daily_plans)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))


@newsletter_router.callback_query(F.data == "toggle_evening_quote")
async def toggle_evening_quote_handler(callback_query: types.CallbackQuery):
    tg_id = str(callback_query.from_user.id)
    settings = await get_or_refresh_user_settings(tg_id)
    settings = await get_or_refresh_user_settings(tg_id, update_evening=not settings.newsletter_good_evening)
    await callback_query.message.edit_reply_markup(reply_markup=get_notification_settings_markup(settings))


@newsletter_router.message(IsNotRegister(), Command("newsletter"))
async def newsletter_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text="Please, register first", parse_mode=ParseMode.HTML,
                           reply_markup=translate_markup)
