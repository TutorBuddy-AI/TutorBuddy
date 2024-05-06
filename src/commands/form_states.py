import asyncio

from commands.choose_speaker import continue_dialogue_with_person
from config import config
from src.database import session
from sqlalchemy import select

from src.config import bot
from src.states import Form, FormCity
from src.filters import IsNotRegister
from src.texts.texts import get_meet_nastya_text, get_meet_bot_text, get_other_native_language_question, get_incorrect_native_language_question, \
    get_chose_some_topics, get_other_goal, get_other_topics, get_chose_some_more_topics, get_meet_bot_message, \
    get_meet_nastya_message
from src.keyboards.form_keyboard import get_choose_native_language_keyboard, get_choose_goal_keyboard, \
    get_choose_english_level_keyboard, get_choose_topic_keyboard, get_choose_bot_keyboard
from src.utils.answer import AnswerRenderer
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.transcriber.text_to_speech import TextToSpeech
from src.database.models.setting import Setting
from src.database.models import Base, UserLocation

from src.utils.user import UserService, UserHelper

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.types import FSInputFile, Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode

from utils.user.schemas import UserInfo

from src.database.models.user import UserLocation
from src.database.session import session

form_router = Router(name=__name__)


async def clean_messages(chat_id: str, message_id: str):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


async def process_start_acquaintance(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await bot.send_photo(
        message.chat.id,
        photo=FSInputFile('./files/choose_name.png'),
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


@form_router.callback_query(F.data == "name_ok", Form.name)
async def process_name_ok(query: types.CallbackQuery, state: FSMContext):
    name = query.from_user.first_name
    await bot.send_message(
        query.message.chat.id,
        "That's great! Nice to meet you 😉",
        parse_mode=ParseMode.HTML,
        reply_markup=AnswerRenderer.get_markup_text_translation_standalone()
    )
    await state.update_data({"name": name})
    await state.set_state(Form.native_language)
    await bot.send_photo(
        query.message.chat.id, photo=FSInputFile('./files/native_lang.png'),
        caption="What is your native language?",
        parse_mode=ParseMode.HTML,
        reply_markup=await get_choose_native_language_keyboard())


@form_router.callback_query(F.data == "not_me", Form.name)
async def process_not_me(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.other_name)
    markup = AnswerRenderer.get_markup_text_translation_standalone()
    await bot.send_message(
        query.message.chat.id,
        "What should I call you then?",
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )


@form_router.message(IsNotRegister(), Form.other_name)
async def process_get_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await bot.send_message(
        message.chat.id,
        "That's great! Nice to meet you 😉",
        parse_mode=ParseMode.HTML,
        reply_markup=AnswerRenderer.get_markup_text_translation_standalone()
    )
    await state.set_state(Form.native_language)
    await bot.send_photo(
        message.chat.id, photo=FSInputFile('./files/native_lang.png'),
        caption="What is your native language?",
        parse_mode=ParseMode.HTML,
        reply_markup=await get_choose_native_language_keyboard())


@form_router.callback_query(Form.native_language, F.data.startswith("native"))
async def process_native_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data({"native_language": query.data.split("_")[1]})
    await state.set_state(Form.goal)

    await bot.send_photo(
        query.message.chat.id, photo=FSInputFile('./files/goal.png'),
        caption="Why are you practicing English?\nWhat's your goal🎯?",
        parse_mode=ParseMode.HTML,
        reply_markup=await get_choose_goal_keyboard())


@form_router.callback_query(Form.native_language, F.data == "other_language")
async def process_start_register_other_language(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_native_language_question(),
                           parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.other_language)


@form_router.message(Form.other_language)
async def process_other_language(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await bot.send_message(message.chat.id, get_incorrect_native_language_question(),
                               parse_mode=ParseMode.HTML)
    else:
        await state.update_data({"native_language": message.text})
        await bot.send_photo(message.chat.id, photo=FSInputFile('./files/goal.png'),
                             caption="Why are you practicing English?\nWhat's your goal 🎯 ?",
                             parse_mode=ParseMode.HTML,
                             reply_markup=await get_choose_goal_keyboard())
        await state.set_state(Form.goal)


@form_router.callback_query(Form.goal, F.data.startswith("goal"))
async def process_goal_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data({"goal": query.data.split("_")[1]})

    await bot.send_photo(query.message.chat.id, photo=FSInputFile('./files/eng_level.png'),
                         caption=f"What is your English level 📶 ?",
                         parse_mode=ParseMode.HTML,
                         reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@form_router.callback_query(Form.goal, F.data == "other_goal")
async def start_process_other_goal_handler(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_goal(),
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone(),
                           parse_mode=ParseMode.HTML)
    await state.set_state(Form.other_goal)


@form_router.message(Form.other_goal, F.text)
async def process_other_goal_handler(message: types.Message, state: FSMContext):
    await state.update_data({"goal": message.text})
    await bot.send_photo(message.chat.id, photo=FSInputFile('./files/eng_level.png'),
                         caption=f"What is your English level 📶 ?",
                         parse_mode=ParseMode.HTML,
                         reply_markup=await get_choose_english_level_keyboard())
    await state.set_state(Form.english_level)


@form_router.callback_query(Form.english_level, F.data.startswith("level"))
async def process_level_handler(query: types.CallbackQuery, state: FSMContext):
    await state.update_data({"english_level": query.data.split("_")[1]})

    await state.set_state(Form.topic)

    await bot.send_photo(query.message.chat.id, photo=FSInputFile('./files/topic.jpg'),
                         caption=get_chose_some_topics(),
                         reply_markup=await get_choose_topic_keyboard(),
                         parse_mode=ParseMode.HTML)


@form_router.message(Form.other_language, state="*")
async def process_city_question(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Which city are you from?")
    await state.set_state("city_question")


@form_router.message(state="city_question")
async def process_city_answer(message: types.Message, state: FSMContext):
    city_name = message.text
    async with session() as db_session:
        existing_location = await db_session.get(UserLocation, str(message.chat.id))
        if existing_location:
            await bot.send_message(message.chat.id, "We already have your city information on record!")
        else:
            user_location = UserLocation(tg_id=str(message.chat.id), city_name=city_name)
            db_session.add(user_location)
            await db_session.commit()
            await bot.send_message(message.chat.id, "Thanks for letting me know!")

    await process_other_language(message, state)


@form_router.callback_query(Form.topic, F.data.startswith("topic"))
async def process_topic_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=await get_choose_topic_keyboard(callback_query))


@form_router.callback_query(Form.topic, F.data == "done")
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
    await state.update_data({"topic": result_text})

    if was_other:
        await state.set_state(Form.additional_topic)
        markup = AnswerRenderer.get_markup_text_translation_standalone()
        await bot.send_message(query.message.chat.id, get_other_topics(),
                               reply_markup=markup, parse_mode=ParseMode.HTML)
    else:
        await state.update_data({"additional_topic": ""})
        await create_user_setup_speaker_choice(query.message, state)


@form_router.message(Form.additional_topic, F.text)
async def process_other_topic_handler(message: types.Message, state: FSMContext):
    await state.update_data({"additional_topic": message.text})
    await create_user_setup_speaker_choice(message, state)


async def create_user_setup_speaker_choice(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    user_info: UserInfo = await UserHelper().group_user_info(state_user_info=state_data, message=message)
    # user_location_info = await UserLocation().get_user_location_info(ip_address=state_data["ip_address"])
    great_markup = AnswerRenderer.get_markup_text_translation_standalone()

    await UserService().create_user(user_info=user_info)  # Когда будет необходим ip, подставить
    # переменную, которая закоменчена выше
    name = user_info["call_name"]
    await bot.send_message(
        message.chat.id,
        f"Great! Nice getting to know you, {name}! I guess it’s my turn to tell you about me.",
        parse_mode=ParseMode.HTML,
        reply_markup=great_markup)

    if config.BOT_TYPE == "original":
        await choose_person(message, state, user_info)
    else:
        await continue_dialogue_with_person(message, state)


async def choose_person(message: Message, state: FSMContext, user_info: UserInfo):
    await asyncio.sleep(1)
    wait_message = await bot.send_message(message.chat.id, f"⏳ TutorBuddy thinks… Please wait",
                                          parse_mode=ParseMode.HTML)

    caption_markup = AnswerRenderer.get_markup_caption_translation_standalone()
    meet_bot_text = get_meet_bot_text()
    audio = await TextToSpeech.get_speech_by_voice(voice="TutorBuddy", text=meet_bot_text)

    await bot.send_photo(
        message.chat.id,
        photo=FSInputFile('./files/meet_bot.png'),
        caption=get_meet_bot_message(),
        parse_mode=ParseMode.HTML,
        reply_markup=caption_markup)
    await bot.delete_message(message.chat.id, wait_message.message_id)

    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            FSInputFile(ogg_file),
            parse_mode=ParseMode.HTML
        )

    wait_message = await bot.send_message(message.chat.id, f"⏳ TutorBuddy thinks… Please wait",
                                          parse_mode=ParseMode.HTML)
    meet_nastya_text = get_meet_nastya_text(user_info["call_name"])
    audio = await TextToSpeech.get_speech_by_voice(voice="Anastasia", text=meet_nastya_text)
    await bot.send_photo(
        message.chat.id,
        photo=FSInputFile('./files/meet_nastya.png'),
        caption=get_meet_nastya_message(user_info["call_name"]),
        parse_mode=ParseMode.HTML,
        reply_markup=caption_markup)
    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            FSInputFile(ogg_file),
            parse_mode=ParseMode.HTML
        )

    await bot.send_message(
        message.chat.id, text="Who would you like to talk to?", parse_mode=ParseMode.HTML,
        reply_markup=await get_choose_bot_keyboard(is_caption=False))

    await bot.delete_message(message.chat.id, wait_message.message_id)
    await state.clear()


@form_router.callback_query(F.data.startswith('dispatch_summary_'))
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
        await bot.send_message(query.message.chat.id, text_true, parse_mode=ParseMode.HTML,
                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))
    else:
        text_false = ("Got it! ✌🏻 In case you change your mind, "
                      "go to Menu and choose 'Summaries', so you can still get the most fresh ones!")
        await bot.send_message(query.message.chat.id, text_false, parse_mode=ParseMode.HTML,
                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))
