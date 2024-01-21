import asyncio

from aiogram.dispatcher import FSMContext
from commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from src.utils.user import UserCreateMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from utils.generate.communication import CommunicationGenerate
from utils.generate.complex_answer_generator.answer_mistakes_generator import AnswerMistakesGenerator
from utils.message import MessageHelper
from utils.message_hint.message_hint_creator import MessageHintCreator
from utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from utils.message_hint.message_hint_service import MessageHintService
from utils.message_history_mistakes.message_mistakes_creator import MessageMistakesCreator
from utils.message_translation import MessageTranslationService
from utils.message_translation.message_translation_creator import MessageTranslationCreator
from utils.paraphrasing import MessageParaphraseService

from aiogram import types, md
from utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_get_text_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)

    if await user_service.was_last_message_sent_two_days_ago():
        await bot.send_sticker(message.chat.id,
                               "CAACAgIAAxkBAAELCClliDpu7gUs1D7IY2VbH0lFGempgwACnUgAAlH1eEtz9YwiWRWyAAEzBA")
        state_data = await state.get_data()
        state_data["sticker_sent"] = True
        await state.update_data(state_data)
    # try to generate AI's answer combined with the list of mistakes
    generated_json = await AnswerMistakesGenerator(
        tg_id=str(message.chat.id),
        prompt=message.text,
        user_message_history=await user_service.get_user_message_history()).generate_message()

    if generated_json:
        written_messages = await UserCreateMessage(
            tg_id=str(message.chat.id),
            prompt=message.text,
            type_message="text"
        ).create_communication_message_text(generated_json["answer"])

        await MessageHelper().group_conversation_info_to_state(state, written_messages)
        await set_message_menu(message, state, generated_json)
    else:
        # json wasn't successfully generated - regenerate answer separately
        generated_text = await CommunicationGenerate(
            tg_id=str(message.chat.id),
            prompt=message.text,
            user_message_history=await user_service.get_user_message_history()).generate_message()

        if generated_text is not None:
            written_messages = await UserCreateMessage(
                tg_id=str(message.chat.id),
                prompt=message.text,
                type_message="text"
            ).create_communication_message_text(generated_text)

            await MessageHelper().group_conversation_info_to_state(state, written_messages)
            await set_message_menu(message, state, {"answer": generated_text})
        else:
            # if both ways of text generation were unsuccessfull - apologize
            generated_text = "Oooops, something wrong. Try request again later..."
            await bot.send_message(message.chat.id, md.escape_md(generated_text))
            await bot.send_sticker(message.chat.id,
                                   "CAACAgIAAxkBAAELCCtliDqXM7eKSq7b5EjbayXem1cB5gACmD0AApmSeUtVQ3oaOv4DxDME")



async def set_message_menu(message: types.Message, state: FSMContext, generated_json: dict):
    generated_text = generated_json["answer"]
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    user_message_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    user_message_buttons = [InlineKeyboardButton(
        '📈 Say it better',
        callback_data="get_paraphrase")]

    if "mistakes" not in generated_json:
        user_message_buttons.append(InlineKeyboardButton(
            f"🔴 My mistakes",
            callback_data="get_mistakes"))
    else:
        if generated_json["mistakes"]:
            user_message_buttons.append(InlineKeyboardButton(
                f"""🔴 My mistakes [{len(generated_json["mistakes"])}]""",
                callback_data="get_mistakes"))

    user_message_markup.row(*user_message_buttons)

    additional_menu_message = await bot.send_message(
        message.chat.id, md.escape_md("Your message menu"), reply_markup=user_message_markup)

    bot_message_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    get_hint_btn = InlineKeyboardButton(
        '💡 Hint',
        callback_data="get_hint")
    get_translation_btn = InlineKeyboardButton(
        '📖 Translate',
        callback_data="get_translation")

    bot_message_markup.row(get_hint_btn, get_translation_btn)

    answer_message = await bot.send_message(
        message.chat.id, md.escape_md(generated_text), reply_markup=bot_message_markup)

    state_data = await state.get_data()
    state_data["additional_menu_message_id"] = additional_menu_message.message_id
    state_data["answer_message_id"] = answer_message.message_id
    await state.update_data(state_data)


async def handle_push_message_button(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if ("answer_message_id" in state_data) and state_data["answer_message_id"]:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id, message_id=state_data["answer_message_id"], reply_markup=None)
        state_data["answer_message_id"] = None
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id, message_id=state_data["additional_menu_message_id"], reply_markup=None)
        state_data["additional_menu_message_id"] = None
    await state.update_data(state_data)
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')


@dp.callback_query_handler(text="get_hint")
async def handle_get_hint(query: CallbackQuery, state: FSMContext):
    message: Message = query.message

    await handle_push_message_button(message, state)

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

    await set_message_menu(message, state, state_data["bot_message_text"])


@dp.callback_query_handler(text="get_mistakes")
async def handle_get_mistakes(query: CallbackQuery, state: FSMContext):
    message = query.message

    await handle_push_message_button(message, state)

    state_data = await state.get_data()

    generated_text = await MessageMistakesCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text()

    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
        state_data, message, generated_text)

    await MessageMistakesService().create_mistakes(mistakes_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await set_message_menu(message, state, state_data["bot_message_text"])


@dp.callback_query_handler(text="get_translation")
async def handle_get_translation(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message

    await handle_push_message_button(message, state)

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id),
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(
        state_data, message, generated_text)

    await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await set_message_menu(message, state, state_data["bot_message_text"])


@dp.callback_query_handler(text=["get_paraphrase"])
async def handle_get_paraphrase(query: CallbackQuery, state: FSMContext):
    message = query.message

    await handle_push_message_button(message, state)

    state_data = await state.get_data()

    generated_text = await MessageParaphraseCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)

    await MessageParaphraseService().create_message_paraphrase(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await set_message_menu(message, state, state_data["bot_message_text"])
