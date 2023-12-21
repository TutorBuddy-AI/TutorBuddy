import asyncio

from src.config import dp, bot
from src.states import Form
from src.filters import IsNotRegister
from src.texts.texts import get_welcome_text, get_choose_bot_text
from src.keyboards import get_keyboard_remove
from src.keyboards.form_keyboard import get_choose_native_language_keyboard, get_choose_goal_keyboard,\
    get_choose_english_level_keyboard, get_choose_topic_keyboard, get_choose_bot_keyboard

from src.utils.user import UserService, UserLocation, UserHelper

from aiogram.dispatcher import FSMContext
from aiogram import types, md
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, InlineKeyboardMarkup


@dp.message_handler(IsNotRegister())
async def process_start_register_user(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)

    await bot.send_message(message.chat.id, await get_welcome_text(), parse_mode=ParseMode.MARKDOWN)

    await asyncio.sleep(3)

    await bot.send_message(message.chat.id, md.escape_md("Let's get to know each other first. What should I call you?"),
                           reply_markup=await get_keyboard_remove())


@dp.message_handler(state=Form.name)
async def process_get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.native_language)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    await bot.send_message(message.chat.id, md.escape_md("What is your native language?"),
                           reply_markup=await get_choose_native_language_keyboard())

@dp.callback_query_handler(lambda query: query.data.startswith("native"), state=Form.native_language)
async def process_native_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(native_language=query.data.split("_")[1])
    await state.set_state(Form.goal)

    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md("Why are you practicing English?"),
                           reply_markup=await get_choose_goal_keyboard())

@dp.callback_query_handler(lambda query: query.data.startswith("goal"), state=Form.goal)
async def process_goal_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(goal=query.data.split("_")[1])
    await state.set_state(Form.english_level)

    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md(f"What is your English level?"),
                           reply_markup=await get_choose_english_level_keyboard())

@dp.callback_query_handler(lambda query: query.data.startswith("level"), state=Form.english_level)
async def process_level_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(english_level=query.data.split("_")[1])
    await state.set_state(Form.topic)

    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md("Choose some interesting topics!"),
                           reply_markup=await get_choose_topic_keyboard())

@dp.callback_query_handler(lambda query: query.data.startswith("topic"), state=Form.topic)
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

@dp.callback_query_handler(text="done", state=Form.topic)
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

    user_info = await UserHelper().group_user_info(state_user_info=state_data, message=query.message)
    # user_location_info = await UserLocation().get_user_location_info(ip_address=state_data["ip_address"])

    await UserService().create_user(user_info=user_info, user_location_info=0)  # Когда будет необходим ip, подставить
                                                                                # переменную, которая закоменчена выше

    await bot.send_message(query.message.chat.id, await get_choose_bot_text(),
                           reply_markup=await get_choose_bot_keyboard())
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 6)
    except:
        pass

    await state.finish()
