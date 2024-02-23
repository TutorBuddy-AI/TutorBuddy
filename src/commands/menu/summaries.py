from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.keyboards.form_keyboard.form_keyboard import get_keyboard_summary_choice
from src.utils.answer import AnswerRenderer


@dp.message_handler(IsRegister(), commands=["summaries"])
async def summaries_handler(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        text=md.escape_md("A quick reminder: news summaries is a format where "
                          "I send you fresh global news and we share opinions on the topic 📃"))
    await bot.send_message(
        message.chat.id,
        text=md.escape_md("I am always willing to share some recent news summaries! "
                          "Do you want me to start sending them from now on?"),
        reply_markup=await get_keyboard_summary_choice(menu=True))


@dp.message_handler(IsNotRegister(), commands=["summaries"])
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text=md.escape_md("Please, register first"), reply_markup=translate_markup)
