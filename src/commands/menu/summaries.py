from aiogram import types, md, Router, F
from aiogram.fsm.context import FSMContext

from src.config import bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.keyboards.form_keyboard.form_keyboard import get_keyboard_summary_choice, get_keyboard_cancel_news_subs, \
    get_keyboard_resume_news_subs
from src.utils.answer import AnswerRenderer
from src.utils.setting.setting_service import SettingService

summaries_router = Router(name=__name__)


@summaries_router.message(IsRegister(), F.commands == ["summaries"])
async def summaries_handler(message: types.Message, state: FSMContext):
    tg_id = message.chat.id
    await bot.send_message(
        tg_id,
        text=md.escape_md("A quick reminder: news summaries is a format where "
                          "I send you fresh global news and we share opinions on the topic 📃"),
        reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True)
    )
    if await SettingService.is_summary_on(str(tg_id)):
        await bot.send_message(
            tg_id,
            text=md.escape_md("I am always willing to share some recent news summaries! "
                              "Do you want me to continue sending them to you or would "
                              "you prefer not to receive them from now on?"),
            reply_markup=await get_keyboard_cancel_news_subs())
    else:
        await bot.send_message(
            tg_id,
            text=md.escape_md("I am always willing to share some recent news summaries! "
                              "Do you want me to start sending them from now on?"),
            reply_markup=await get_keyboard_resume_news_subs())


@summaries_router.message(IsNotRegister(), F.commands == ["summaries"])
async def summaries_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text=md.escape_md("Please, register first"), reply_markup=translate_markup)
