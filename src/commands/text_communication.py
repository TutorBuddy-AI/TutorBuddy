import asyncio
from sqlalchemy import select
from aiogram.dispatcher import FSMContext
from commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from aiogram.types import CallbackQuery, Message
from utils.message import MessageHelper
from utils.message_hint.message_hint_creator import MessageHintCreator
from utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from utils.message_hint.message_hint_service import MessageHintService
from utils.message_history_mistakes.message_mistakes_creator import MessageMistakesCreator
from utils.message_translation import MessageTranslationService
from utils.message_translation.message_translation_creator import MessageTranslationCreator
from utils.paraphrasing import MessageParaphraseService
from src.database import session
from src.database.models import User
from aiogram import types, md
from utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator
from utils.user import UserService


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_get_text_message(message: types.Message, state: FSMContext):
    user_servic = UserService()
    user_info = await user_servic.get_user_info(tg_id=message.chat.id)


    if user_info:
        speaker = user_info["speaker"]
    else:
        speaker = "Anastasia"
    query_speaker = select(User).where(User.speaker == speaker)
    result_speaker = await session.execute(query_speaker)
    speaker_data = result_speaker.scalar()
    speaker_name = speaker_data.speaker if speaker_data else "Anastasia"

    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    user_service = UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=message.text,
        type_message="text"
    )

    wait_message = await bot.send_message(message.chat.id, f"⏳ {speaker_name} thinks… Please wait")


    await bot.delete_message(message.chat.id, wait_message.message_id)
    handler = CommunicationHandler(message, state, bot)

    await handler.handle_text_message()


@dp.callback_query_handler(text="request_hint")
async def handle_get_hint(query: CallbackQuery, state: FSMContext):
    message: Message = query.message
    handler = CommunicationHandler(message, state, bot)

    state_data = await state.get_data()
    if "sticker_sent" not in state_data:
        await bot.send_sticker(query.message.chat.id,
                               "CAACAgIAAxkBAAELBollhzvGQUHW5zqXIk8i-FCo0KcvvgACiTwAAj2PgUvXNnwncAPTwjME")
        state_data["sticker_sent"] = True
        await state.update_data(state_data)

    generated_text = await MessageHintCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)

    await MessageHintService().create_message_hint(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@dp.callback_query_handler(text="request_mistakes")
async def handle_get_mistakes(query: CallbackQuery, state: FSMContext):
    message = query.message

    handler = CommunicationHandler(message, state, bot)

    state_data = await state.get_data()

    generated_text = await MessageMistakesCreator(
        tg_id=str(message.chat.id),
        message_text = state_data["user_message_text"]
    ).create_communication_message_text()

    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
        state_data, message, generated_text)

    await MessageMistakesService().create_mistakes(mistakes_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())

@dp.callback_query_handler(text="request_translation")
async def handle_get_translation(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message

    handler = CommunicationHandler(message, state, bot)

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(
        state_data, message, generated_text)

    await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@dp.callback_query_handler(text=["request_paraphrase"])
async def handle_get_paraphrase(query: CallbackQuery, state: FSMContext):
    message = query.message

    handler = CommunicationHandler(message, state, bot)

    state_data = await state.get_data()

    generated_text = await MessageParaphraseCreator(
        tg_id=str(message.chat.id),
        message_text = state_data["user_message_text"]
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)

    await MessageParaphraseService().create_message_paraphrase(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))

    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())
