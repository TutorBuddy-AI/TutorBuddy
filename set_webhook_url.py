import logging

from src.config import bot, config
from src.config.initialize import dp

from aiogram.utils.executor import start_webhook


async def on_startup(dispatcher):
    await bot.set_webhook(url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}", secret_token=config.WEBHOOK_SECRET_TOKEN)
    logging.info("Bot starting")
    logging.info("Dispatcher - %r", dispatcher)

# async def on_shutdown(dispatcher):
#     await bot.delete_webhook()


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
    )