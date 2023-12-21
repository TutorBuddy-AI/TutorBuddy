from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.keyboards.form_keyboard import get_choose_topic_keyboard
from src.states import FormTopic
from src.utils.user import UserService


@dp.message_handler(commands=["changetopic"])
async def change_topic_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    await bot.send_message(message.chat.id, f"Which topic would you like to discuss instead? 🤓",
                           reply_markup=await get_choose_topic_keyboard())


@dp.callback_query_handler(lambda query: query.data == "change_topic")
async def change_topic_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md(f"Which topic would you like to discuss instead? 🤓"),
                           reply_markup=await get_choose_topic_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("topic"), state=FormTopic.new_topic)
async def process_topic_handler(callback_query: types.CallbackQuery):
    keyboard = callback_query.message.reply_markup.inline_keyboard

    for row in keyboard:
        for button in row:
            if button.callback_data == callback_query.data and button.text.startswith("✅ "):
                button.text = button.text.replace("✅ ", "")
                break

            if button.callback_data == callback_query.data and not button.text.startswith("✅ "):
                button.text = "✅ " + button.text
                break

    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard))


@dp.callback_query_handler(text="done", state=FormTopic.new_topic)
async def process_done_command(query: types.CallbackQuery, state: FSMContext):
    keyboard = query.message.reply_markup.inline_keyboard
    result_text = ""

    for row_button in keyboard:
        for button in row_button:
            text = button.text.split()

            if text[0].startswith("✅"):
                result_text += text[1] + " "

    await state.update_data(topic=result_text)

    state_data = await state.get_data()

    await UserService().change_topic(tg_id=str(query.message.chat.id), new_topic=state_data["topic"])

    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 2)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md("The topics has been successfully changed!\n"
                                                               f"Current topics: {state_data['topic']}"),
                           reply_markup=await get_go_back_inline_keyboard())

    await state.finish()
