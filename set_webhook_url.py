import logging

from aiogram.types import BotCommand

from src.config import bot, config
from src.config.initialize import dp

from aiogram.utils.executor import start_webhook


async def on_startup(dispatcher):
    if config.WEBHOOK_SECRET_TOKEN:
        await bot.set_webhook(url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}", secret_token=config.WEBHOOK_SECRET_TOKEN)
    else:
        await bot.set_webhook(url=f"{config.WEBHOOK_URL}")
    logging.info("Bot starting")
    logging.info("Dispatcher - %r", dispatcher)

    bot_commands = [
        BotCommand(command="/restart", description="Restart the bot"),
        BotCommand(command="/scenario", description="Choose a scenario (soon)"),
        BotCommand(command="/changetopic", description="Change topic"),
        BotCommand(command="/editprofile", description="Edit profile"),
        BotCommand(command="/persona", description="Choose a persona to chat"),
        BotCommand(command="/all_mistakes", description="Show all my mistakes"),
        BotCommand(command="/support", description="Contact support"),
        BotCommand(command="/feedback", description="Leave feedback"),
    ]
    await bot.set_my_commands(bot_commands)

# async def on_shutdown(dispatcher):
#     await bot.delete_webhook()


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
    )