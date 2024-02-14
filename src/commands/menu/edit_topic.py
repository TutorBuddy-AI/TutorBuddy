from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.keyboards.form_keyboard import get_choose_topic_keyboard
from src.states import FormTopic
from src.utils.user import UserService
from src.texts.texts import get_chose_some_more_topics, get_other_topics


@dp.message_handler(commands=["changetopic"])
async def change_topic_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    await bot.send_photo(message.chat.id, photo=types.InputFile('./files/topic.jpg'), caption=md.escape_md(f"Which topic would you like to discuss instead? 🤓"),
                           reply_markup=await get_choose_topic_keyboard())


@dp.callback_query_handler(lambda query: query.data == "change_topic")
async def change_topic_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    await bot.send_message(query.message.chat.id, md.escape_md(f"Which topic would you like to discuss instead? 🤓"),
                           reply_markup=await get_choose_topic_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("topic"), state=FormTopic.new_topic)
async def process_topic_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=await get_choose_topic_keyboard(callback_query))


@dp.callback_query_handler(text="done", state=FormTopic.new_topic)
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


@dp.callback_query_handler(text="done", state=FormTopic.new_topic)
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
        await bot.send_message(query.message.chat.id, get_chose_some_more_topics(),
                               reply_markup=await get_choose_topic_keyboard())
    else:
        await process_topics(query, state, result_text, was_other)


async def process_topics(query: types.CallbackQuery, state: FSMContext, result_text, was_other):
    async with state.proxy() as data:
        data["topic"] = result_text

    if was_other:
        await state.set_state(FormTopic.new_additional_topic)
        await bot.send_message(query.message.chat.id, get_other_topics())
    else:
        async with state.proxy() as data:
            data["additional_topic"] = ""
        await create_user_setup_speaker_choice(query.message, state)


@dp.message_handler(state=FormTopic.new_additional_topic)
async def process_other_topic_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["additional_topic"] = message.text
    await create_user_setup_speaker_choice(message, state)


async def create_user_setup_speaker_choice(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    await UserService().change_topic(
        tg_id=str(message.chat.id), new_topic=state_data["topic"], new_additional_topic=state_data["additional_topic"])

    await bot.send_message(
        message.chat.id,
        md.escape_md(
            "The topics has been successfully changed!\n"
            f"Current topics: {state_data['topic']} {state_data['additional_topic']}"),
        reply_markup=await get_go_back_inline_keyboard())

    await state.finish()