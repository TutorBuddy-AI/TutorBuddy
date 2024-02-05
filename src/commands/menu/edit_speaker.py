from aiogram import types, md
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.utils.user import UserService
from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard


@dp.message_handler(commands=["persona"])
async def edit_speaker_handler(message: types.Message):
    persona_kb = InlineKeyboardMarkup(row_width=1)

    nastya = InlineKeyboardButton(text='👩🏻‍🚀 Choose Anastasia', callback_data='speaker_Anastasia')
    bot_tutor = InlineKeyboardButton(text='🤖 Choose TutorBuddy', callback_data='speaker_Tutor Bot')

    go_back = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    persona_kb.add(nastya).add(bot_tutor).add(go_back)

    await bot.send_message(message.chat.id, md.escape_md("Who would you like to talk with? 💌"),
                           reply_markup=persona_kb)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.callback_query_handler(lambda query: query.data.startswith("speaker"))
async def change_speaker_query_handler(query: CallbackQuery):
    await UserService().change_speaker(tg_id=str(query.message.chat.id), new_speaker=query.data.split('_')[1])
    await bot.send_message(query.message.chat.id, md.escape_md(f"Great! Your current person is"
                                                               f" {query.data.split('_')[1]}"),
                           reply_markup=await get_go_back_inline_keyboard())

