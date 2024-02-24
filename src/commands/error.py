from aiogram import md
from aiogram.utils.exceptions import BadRequest

from src.config import dp, bot


@dp.errors_handler()
async def error_handler(update, error: Exception) -> None:
    await dp.current_state().finish()
    if str(error) == "Voice_messages_forbidden":
        if update.message:
            await bot.send_message(
                update.message.chat.id,
                md.escape_md("Please, enable voice messages"))
    else:
        if update.message:
            await bot.send_message(
                update.message.chat.id,
                md.escape_md("Sorry, something went wrong on our side. Please, use /cancel command to reset")
            )
        if update.edited_message:
            await bot.send_message(
                update.edited_message.chat.id,
                md.escape_md("Sorry, something went wrong on our side. Please, use /cancel command to reset"))

        if update.callback_query:
            if update.callback_query.message:
                await bot.send_message(
                    update.callback_query.message.chat.id,
                    md.escape_md("Sorry, something went wrong on our side. Please, use /cancel command to reset"))
