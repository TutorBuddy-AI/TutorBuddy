import asyncio

from src.config import dp, bot
from src.states import Form
from src.filters import IsNotRegister
from src.texts.texts import get_welcome_text, get_choose_bot_text, get_welcome_text_before_start, \
    get_lets_know_each_other, get_other_native_language_question, get_incorrect_native_language_question, \
    get_chose_some_topics, get_other_goal, get_other_topics, get_choose_buddy_text1, get_choose_buddy_text3, \
    get_choose_buddy_text2, get_chose_some_more_topics
from src.keyboards.form_keyboard import get_choose_native_language_keyboard, get_choose_goal_keyboard, \
    get_choose_english_level_keyboard, get_choose_topic_keyboard, get_choose_bot_keyboard

from src.utils.user import UserService, UserHelper

from aiogram.dispatcher import FSMContext
from aiogram import types, md
from aiogram.types import InputFile, CallbackQuery
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


async def clean_messages(chat_id: str, message_id: str):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


@dp.message_handler(IsNotRegister())
async def process_start_register_user(message: types.Message):
    """
    Function to explain bot idea for new users
    """
    welcome_text = get_welcome_text()

    await bot.send_message(message.chat.id, welcome_text)
    await bot.send_animation(
        message.chat.id,
        animation=InputFile("./files/tutorbuddy_welcome.gif")
    )
    await bot.send_message(
        message.chat.id,
        get_lets_know_each_other()
    )
    await process_start_acquaintance(message, state)


@dp.callback_query_handler(text=["start"])
async def process_start_acquaintance(query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.name)
    await bot.send_message(
        query.chat.id,
        f"Do you want me to call you '{query.from_user.first_name}' or do you prefer a different format?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(f"{query.from_user.first_name} - good 👍", callback_data="name_ok")],
            [InlineKeyboardButton("No, call me…✍️🏻", callback_data="not_me")]
        ])
    )


@dp.callback_query_handler(lambda query: query.data == "name_ok", state=Form.name)
async def process_name_ok(query: types.CallbackQuery, state: FSMContext):
    name = query.from_user.first_name
    async with state.proxy() as data:
        data["name"] = name
    await state.set_state(Form.native_language)
    await bot.send_message(
        query.message.chat.id, md.escape_md("What is your native language?"),
        reply_markup=await get_choose_native_language_keyboard())

@dp.callback_query_handler(lambda query: query.data == "not_me", state=Form.name)
async def process_not_me(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.other_name)
    await bot.send_message(
        query.message.chat.id,
        "I understand, in messengers we often improvise\) What's the best way for me to address you?",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(state=Form.other_name)
async def process_get_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data["name"] = message.text

    await say_hello(name, message.chat.id)
    await state.set_state(Form.native_language)
    await bot.send_message(
        message.chat.id, md.escape_md("What is your native language?"),
        reply_markup=await get_choose_native_language_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("native"), state=Form.native_language)
async def process_native_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["native_language"] = query.data.split("_")[1]
    await state.set_state(Form.goal)

    await bot.send_message(
        query.message.chat.id, md.escape_md("Why are you practicing English?"),
        reply_markup=await get_choose_goal_keyboard())


@dp.callback_query_handler(lambda query: query.data == "other_language", state=Form.native_language)
async def process_start_register_other_language(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_native_language_question(),
                           reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.other_language)


@dp.message_handler(state=Form.other_language)
async def process_other_language(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await bot.send_message(message.chat.id, get_incorrect_native_language_question())
    else:
        async with state.proxy() as data:
            data["native_language"] = message.text
        await bot.send_message(message.chat.id, md.escape_md("Why are you practicing English?"),
                               reply_markup=await get_choose_goal_keyboard())
        await state.set_state(Form.goal)


@dp.callback_query_handler(lambda query: query.data.startswith("goal"), state=Form.goal)
async def process_goal_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["goal"] = query.data.split("_")[1]

    await bot.send_message(query.message.chat.id, md.escape_md(f"What is your English level?🧑🏽‍🏫👩🏻‍🏫"),
                           reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@dp.callback_query_handler(lambda query: query.data == "other_goal", state=Form.goal)
async def start_process_other_goal_handler(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_goal(),
                           reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.other_goal)


@dp.message_handler(state=Form.other_goal)
async def process_other_goal_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["goal"] = message.text
    await bot.send_message(message.chat.id, md.escape_md(f"What is your English level?🧑🏽‍🏫👩🏻‍🏫"),
                           reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@dp.callback_query_handler(lambda query: query.data.startswith("level"), state=Form.english_level)
async def process_level_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["english_level"] = query.data.split("_")[1]

    await state.set_state(Form.topic)

    await bot.send_message(query.message.chat.id, get_chose_some_topics(),
                           reply_markup=await get_choose_topic_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("topic"), state=Form.topic)
async def process_topic_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=await get_choose_topic_keyboard(callback_query))


@dp.callback_query_handler(text="done", state=Form.topic)
async def process_done_command(query: types.CallbackQuery, state: FSMContext):
    keyboard = query.message.reply_markup.inline_keyboard
    result_text = ""
    was_other = False
    topics_num = 0
    for row_button in keyboard:
        for button in row_button:
            text = button.text.split()

            if text[0].startswith("✅"):
                if text[1] == "Other":
                    was_other = True
                else:
                    topics_num += 1
                    result_text += text[1] + " "
    if topics_num <= 2:
        await bot.answer_callback_query(query.id, get_chose_some_more_topics(), show_alert=True)
    else:
        await process_topics(query, state, result_text, was_other)


async def process_topics(query: types.CallbackQuery, state: FSMContext, result_text, was_other):
    async with state.proxy() as data:
        data["topic"] = result_text

    if was_other:
        await state.set_state(Form.additional_topic)
        await bot.send_message(query.message.chat.id, get_other_topics())
    else:
        async with state.proxy() as data:
            data["additional_topic"] = ""
        await create_user_setup_speaker_choice(query.message, state)


@dp.message_handler(state=Form.additional_topic)
async def process_other_topic_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["additional_topic"] = message.text
    await create_user_setup_speaker_choice(message, state)


async def create_user_setup_speaker_choice(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    user_info = await UserHelper().group_user_info(state_user_info=state_data, message=message)
    # user_location_info = await UserLocation().get_user_location_info(ip_address=state_data["ip_address"])

    await UserService().create_user(user_info=user_info)  # Когда будет необходим ip, подставить
    # переменную, которая закоменчена выше
    await bot.send_message(message.chat.id, get_choose_buddy_text1())
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id, get_choose_buddy_text2())
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id, get_choose_buddy_text3())
    await asyncio.sleep(2)
    await bot.send_animation(
        message.chat.id, animation=InputFile("./files/tutorbuddy_choose.gif"),
        reply_markup=await get_choose_bot_keyboard())

    await state.finish()
