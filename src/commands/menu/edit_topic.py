from aiogram import types, md, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from src.config import bot
from src.filters.is_not_register_filter import IsRegister, IsNotRegister
from src.keyboards import get_go_back_inline_keyboard
from src.keyboards.form_keyboard import get_choose_topic_keyboard
from src.states import FormTopic
from src.utils.answer import AnswerRenderer
from src.utils.user import UserService
from src.texts.texts import get_chose_some_more_topics, get_other_topics

edit_topic_router = Router(name=__name__)


@edit_topic_router.message(IsRegister(), Command("changetopic"))
async def change_topic_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    await bot.send_photo(message.chat.id, photo=FSInputFile('./files/topic.jpg'),
                         caption=f"Which topic would you like to discuss instead? 🤓",
                         parse_mode=ParseMode.HTML,
                         reply_markup=await get_choose_topic_keyboard(for_user=True))


@edit_topic_router.message(IsNotRegister(), Command("changetopic"))
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text="Please, register first", parse_mode=ParseMode.HTML,
                           reply_markup=translate_markup)


@edit_topic_router.callback_query(F.data == "change_topic")
async def change_topic_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(FormTopic.new_topic)

    await bot.send_message(query.message.chat.id, f"Which topic would you like to discuss instead? 🤓",
                           parse_mode=ParseMode.HTML,
                           reply_markup=await get_choose_topic_keyboard(for_user=True, is_caption=False))


@edit_topic_router.callback_query(F.data.startswith("topic"), FormTopic.new_topic)
async def process_topic_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=await get_choose_topic_keyboard(callback_query, for_user=True,
                                                                                     is_caption=False))


@edit_topic_router.callback_query(F.data == "done", FormTopic.new_topic)
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
    if topics_num < 1:
        await bot.answer_callback_query(query.id, get_chose_some_more_topics(), show_alert=True)
    else:
        await process_topics(query, state, result_text, was_other)


@edit_topic_router.callback_query(F.data == "done", FormTopic.new_topic)
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

    if topics_num < 1:
        await bot.send_message(query.message.chat.id, get_chose_some_more_topics(),
                               reply_markup=await get_choose_topic_keyboard(for_user=True, is_caption=False))
    else:
        await process_topics(query, state, result_text, was_other)


async def process_topics(query: types.CallbackQuery, state: FSMContext, result_text, was_other):
    await state.update_data({"topic": result_text})

    if was_other:
        await state.set_state(FormTopic.new_additional_topic)
        await bot.send_message(query.message.chat.id, get_other_topics())
    else:
        await state.update_data({"additional_topic": ""})
        await create_user_setup_speaker_choice(query.message, state)


@edit_topic_router.message(FormTopic.new_additional_topic)
async def process_other_topic_handler(message: types.Message, state: FSMContext):
    await state.update_data({"additional_topic": message.text})
    await create_user_setup_speaker_choice(message, state)


async def create_user_setup_speaker_choice(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    await UserService().change_topic(
        tg_id=str(message.chat.id), new_topic=state_data["topic"], new_additional_topic=state_data["additional_topic"])

    await bot.send_message(
        message.chat.id,
        "The topics has been successfully changed!\n"
        f"Current topics: {state_data['topic']} {state_data['additional_topic']}",
        parse_mode=ParseMode.HTML,
        reply_markup=await get_go_back_inline_keyboard())

    await state.clear()
