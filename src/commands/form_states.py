import asyncio
from src.database import session
from sqlalchemy import select

from src.config import bot
from src.states import Form
from src.filters import IsNotRegister
from src.texts.texts import get_welcome_text, get_meet_nastya_text, \
    get_other_native_language_question, get_incorrect_native_language_question, \
    get_chose_some_topics, get_other_goal, get_other_topics, get_chose_some_more_topics, \
    get_meet_bot_message, get_meet_bot_text, get_meet_nastya_message
from src.keyboards.form_keyboard import get_choose_native_language_keyboard, get_choose_goal_keyboard, \
    get_choose_english_level_keyboard, get_choose_topic_keyboard, get_choose_bot_keyboard
from src.utils.answer import AnswerRenderer
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.transcriber.text_to_speech import TextToSpeech
from src.database.models.setting import Setting

from src.utils.user import UserService, UserHelper, UserCreateMessage

from aiogram.fsm.context import FSMContext
from aiogram import types, md, Router, F
from aiogram.types import InputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode

form_router = Router(name=__name__)


async def clean_messages(chat_id: str, message_id: str):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


@form_router.message(IsNotRegister())
async def process_start_register_user(message: types.Message, state: FSMContext):
    """
    Function to explain bot idea for new users
    """
    welcome_text = get_welcome_text()
    caption_markup = AnswerRenderer.get_markup_caption_translation_standalone()

    await bot.send_photo(
        message.chat.id,
        caption=welcome_text,
        photo=InputFile("./files/tutorbuddy_welcome.png"),
        reply_markup=caption_markup
    )
    await asyncio.sleep(2)
    await process_start_acquaintance(message, state)


@form_router.callback_query(F.text == ["start"])
async def process_start_acquaintance(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile('./files/choose_name.png'),
        caption=f"Let's get to know each other first. "
                f"Is it okay if I call you '{message.from_user.first_name}'?\n"
                f"<i>Make sure your name is in English.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{message.from_user.first_name} - is just fine 👋🏻", callback_data="name_ok")],
            [InlineKeyboardButton(text="No, you'd better call me...", callback_data="not_me")],
            [AnswerRenderer.get_button_caption_translation_standalone()]
        ])
    )


@form_router.callback_query(F.query.data == "name_ok", F.state == Form.name)
async def process_name_ok(query: types.CallbackQuery, state: FSMContext):
    name = query.from_user.first_name
    await bot.send_message(
        query.message.chat.id,
        md.escape_md("That's great! Nice to meet you 😉"),
        reply_markup=AnswerRenderer.get_markup_text_translation_standalone()
    )
    async with state.proxy() as data:
        data["name"] = name
    await state.set_state(Form.native_language)
    await bot.send_photo(
        query.message.chat.id, photo=types.InputFile('./files/native_lang.png'),
        caption=md.escape_md("What is your native language?"),
        reply_markup=await get_choose_native_language_keyboard())


@form_router.callback_query(F.query.data == "not_me", F.state == Form.name)
async def process_not_me(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.other_name)
    markup = AnswerRenderer.get_markup_text_translation_standalone()
    await bot.send_message(
        query.message.chat.id,
        md.escape_md("What should I call you then?"),
        reply_markup=markup
    )


@form_router.message(F.state == Form.other_name)
async def process_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await bot.send_message(
        message.chat.id,
        md.escape_md("That's great! Nice to meet you 😉"),
        reply_markup=AnswerRenderer.get_markup_text_translation_standalone()
    )
    await state.set_state(Form.native_language)
    await bot.send_photo(
        message.chat.id, photo=types.InputFile('./files/native_lang.png'),
        caption=md.escape_md("What is your native language?"),
        reply_markup=await get_choose_native_language_keyboard())


@form_router.callback_query(F.query.data.startswith("native"), F.state == Form.native_language)
async def process_native_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["native_language"] = query.data.split("_")[1]
    await state.set_state(Form.goal)

    await bot.send_photo(
        query.message.chat.id, photo=types.InputFile('./files/goal.png'),
        caption=md.escape_md("Why are you practicing English?\nWhat's your goal🎯?"),
        reply_markup=await get_choose_goal_keyboard())


@form_router.callback_query(F.query.data == "other_language", F.state == Form.native_language)
async def process_start_register_other_language(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_native_language_question(),
                           reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.other_language)


@form_router.message(F.state == Form.other_language)
async def process_other_language(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await bot.send_message(message.chat.id, get_incorrect_native_language_question())
    else:
        async with state.proxy() as data:
            data["native_language"] = message.text
        await bot.send_photo(message.chat.id, photo=types.InputFile('./files/goal.png'),
                             caption=md.escape_md("Why are you practicing English?\nWhat's your goal 🎯 ?"),
                             reply_markup=await get_choose_goal_keyboard())
        await state.set_state(Form.goal)


@form_router.callback_query(F.query.data.startswith("goal"), F.state == Form.goal)
async def process_goal_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["goal"] = query.data.split("_")[1]

    await bot.send_photo(query.message.chat.id, photo=types.InputFile('./files/eng_level.png'),
                         caption=md.escape_md(f"What is your English level 📶 ?"),
                         reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@form_router.callback_query(F.query.data == "other_goal", F.state == Form.goal)
async def start_process_other_goal_handler(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_goal(),
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone())
    await state.set_state(Form.other_goal)


@form_router.message(F.state == Form.other_goal)
async def process_other_goal_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["goal"] = message.text
    await bot.send_photo(message.chat.id, photo=types.InputFile('./files/eng_level.png'),
                         caption=md.escape_md(f"What is your English level 📶 ?"),
                         reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@form_router.callback_query(F.query.data.startswith("level"), F.state == Form.english_level)
async def process_level_handler(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["english_level"] = query.data.split("_")[1]

    await state.set_state(Form.topic)

    await bot.send_photo(query.message.chat.id, photo=types.InputFile('./files/topic.jpg'),
                         caption=get_chose_some_topics(),
                         reply_markup=await get_choose_topic_keyboard())


@form_router.callback_query(F.query.data.startswith("topic"), F.state == Form.topic)
async def process_topic_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=await get_choose_topic_keyboard(callback_query))


@form_router.callback_query(F.text == "done", F.state == Form.topic)
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


async def process_topics(query: types.CallbackQuery, state: FSMContext, result_text, was_other):
    async with state.proxy() as data:
        data["topic"] = result_text

    if was_other:
        await state.set_state(Form.additional_topic)
        markup = AnswerRenderer.get_markup_text_translation_standalone()
        await bot.send_message(query.message.chat.id, get_other_topics(), reply_markup=markup)
    else:
        async with state.proxy() as data:
            data["additional_topic"] = ""
        await create_user_setup_speaker_choice(query.message, state)


@form_router.message(F.state == Form.additional_topic)
async def process_other_topic_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["additional_topic"] = message.text
    await create_user_setup_speaker_choice(message, state)


async def create_user_setup_speaker_choice(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    user_info = await UserHelper().group_user_info(state_user_info=state_data, message=message)
    # user_location_info = await UserLocation().get_user_location_info(ip_address=state_data["ip_address"])
    great_markup = AnswerRenderer.get_markup_text_translation_standalone()

    await UserService().create_user(user_info=user_info)  # Когда будет необходим ip, подставить
    # переменную, которая закоменчена выше
    name = user_info["call_name"]
    await bot.send_message(
        message.chat.id,
        md.escape_md(f"Great! Nice getting to know you, {name}! I guess it’s my turn to tell you about me."),
        reply_markup=great_markup)
    await asyncio.sleep(1)

    caption_markup = AnswerRenderer.get_markup_caption_translation_standalone()
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile('./files/meet_bot.png'),
        caption=get_meet_bot_message(),
        reply_markup=caption_markup)

    meet_bot_text = get_meet_bot_text()
    audio = await TextToSpeech.get_speech_by_voice(voice="TutorBuddy", text=meet_bot_text)
    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            types.InputFile(ogg_file),
            parse_mode=ParseMode.HTML
        )

    meet_nastya_text = get_meet_nastya_text(user_info["call_name"])
    audio = await TextToSpeech.get_speech_by_voice(voice="Anastasia", text=meet_nastya_text)
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile('./files/meet_nastya.png'),
        caption=get_meet_nastya_message(user_info["call_name"]),
        reply_markup=caption_markup)
    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            types.InputFile(ogg_file),
            parse_mode=ParseMode.HTML
        )

    await bot.send_message(
        message.chat.id, text=md.escape_md("Who would you like to talk to?"),
        reply_markup=await get_choose_bot_keyboard())
    await state.clear()


@form_router.callback_query(F.query.data.startswith('dispatch_summary_'))
async def handler_choice_summary(query: types.CallbackQuery, state: FSMContext):
    chat_id = query.message.chat.id

    select_query = select(Setting).where(Setting.tg_id == str(chat_id))
    result = await session.execute(select_query)
    user = result.scalars().first()

    user_answer = True if query.data == "dispatch_summary_true" else False
    if user:
        user.summary_on = user_answer
        user.summary_answered = True
        await session.commit()
    else:
        session.add(Setting(tg_id=str(chat_id), summary_on=user_answer, summary_answered=True))
        await session.commit()
    if user_answer:
        text_true = ("Deal! Looking forward to discuss the most up-to-date news ⚡ "
                     "In case you change your mind, you may refuse to receive summaries anytime: "
                     "go to Menu and choose 'Summaries'.")
        await bot.send_message(query.message.chat.id, md.escape_md(text_true),
                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))
    else:
        text_false = ("Got it! ✌🏻 In case you change your mind, "
                      "go to Menu and choose 'Summaries', so you can still get the most fresh ones!")
        await bot.send_message(query.message.chat.id, md.escape_md(text_false),
                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))
