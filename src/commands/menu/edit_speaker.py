from aiogram import types, md, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.filters.is_not_register_filter import IsRegister, IsNotRegister
from src.utils.answer import AnswerRenderer
from src.utils.user import UserService
from src.config import bot
from src.keyboards import get_go_back_inline_keyboard

edit_speaker_router = Router(name=__name__)


@edit_speaker_router.message(IsRegister(), F.commands == ["persona"])
async def edit_speaker_handler(message: types.Message):

    nastya = InlineKeyboardButton(text='💁🏻‍♀️ Anastasia', callback_data='speaker_Anastasia')
    bot_tutor = InlineKeyboardButton(text='🤖 TutorBuddy', callback_data='speaker_TutorBuddy')

    go_back = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')
    persona_kb = InlineKeyboardMarkup(inline_keyboard=[
        [bot_tutor], [nastya], [go_back], [AnswerRenderer.get_button_text_translation_standalone(for_user=True)]])

    await bot.send_message(message.chat.id, md.escape_md("Who would you like to talk with? 💌"),
                           reply_markup=persona_kb)


@edit_speaker_router.message(IsNotRegister(), F.commands == ["persona"])
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text=md.escape_md("Please, register first"), reply_markup=translate_markup)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


@edit_speaker_router.callback_query(F.query.data.startswith("speaker"))
async def change_speaker_query_handler(query: CallbackQuery):
    await UserService().change_speaker(tg_id=str(query.message.chat.id), new_speaker=query.data.split('_')[1])
    await bot.send_message(query.message.chat.id, md.escape_md(f"Great! Your current person is"
                                                               f" {query.data.split('_')[1]}"),
                           reply_markup=await get_go_back_inline_keyboard())

