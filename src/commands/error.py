import logging
import traceback

from aiogram import md, Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Update, ErrorEvent

from src.config import dp, bot

error_router = Router(name=__name__)


async def clean_context(chat_id: int, user_id: int):
    context = dp.fsm.resolve_context(
        bot=bot, chat_id=chat_id, user_id=user_id
    )
    await context.clear()


@error_router.error()
async def error_handler(event: ErrorEvent) -> None:
    logging.info(traceback.print_exception(event.exception))
    update = event.update
    if str(event.exception) == "Voice_messages_forbidden":
        if update.message:
            await bot.send_message(
                update.message.chat.id,
                "Please, enable voice messages",
                parse_mode=ParseMode.HTML)
    else:
        if update.message:
            await bot.send_message(
                update.message.chat.id,
                "Sorry, something went wrong on our side. Please, use /cancel command to reset",
                parse_mode=ParseMode.HTML
            )
            await clean_context(update.message.chat.id, update.message.from_user.id)

        if update.callback_query:
            if update.callback_query.message:
                await bot.send_message(
                    update.callback_query.message.chat.id,
                    "Sorry, something went wrong on our side. Please, use /cancel command to reset",
                    parse_mode=ParseMode.HTML)
                await clean_context(update.callback_query.message.chat.id, update.callback_query.from_user.id)
