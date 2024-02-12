from aiogram import md

from src.config import dp, bot
@dp.errors_handler()
async def error_handler(update, error) -> None:
    await dp.current_state().finish()
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
