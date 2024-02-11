import traceback

from aiogram.types import BotCommand

from config import config
from src.config import dp, bot
from src.commands.form_states import process_start_register_user, process_get_name
from src.filters import IsNotRegister
from src.states import Form
from src.utils.newsletter.newsletter import Newsletter
from aiogram import types

import logging

from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    if config.WEBHOOK_SECRET_TOKEN:
        await bot.set_webhook(
            url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
            secret_token=config.WEBHOOK_SECRET_TOKEN,
            drop_pending_updates=True)
    else:
        await bot.set_webhook(
            url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
            drop_pending_updates=True
        )

    bot_commands = [
        BotCommand(command="/restart", description="⚙ Restart the bot"),
        BotCommand(command="/scenario", description="🎬 Choose a scenario (soon)"),
        BotCommand(command="/changetopic", description="🔁 Change topic"),
        BotCommand(command="/editprofile", description="✏ Edit profile"),
        BotCommand(command="/persona", description="👥 Choose a persona to chat"),
        BotCommand(command="/all_mistakes", description="🔴 Show all my mistakes"),
        BotCommand(command="/support", description="👨💻 Contact support"),
        BotCommand(command="/feedback", description="💬 Leave feedback"),
    ]
    await bot.set_my_commands(bot_commands)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)
    bot.get_session().close()


@app.post(f"/webhook")
async def receive_update(update: Dict, request: Request):
    update_obj = types.Update(**update)
    logging.info(f"Update: {update_obj}")
    try:
        if update_obj.message:
            source = update_obj.message.get_args()
            context = dp.current_state(chat=update_obj.message.chat.id, user=update_obj.message.chat.id)
            data = await context.get_data()
            data["ip_address"] = None
            data["source"] = source if source is not None else None
            data["tg_language"] = update_obj.message.from_user.language_code
            await context.update_data(data)
        await dp.process_update(update_obj)
    except:
        traceback.print_exc()
    finally:
        pass
    return {"status_code": 200}


@app.get('/start_newsletter')
async def send_newsletter():
    try:
        await Newsletter().send_newsletter()
        return {'message': 'Newsletter sent'}
    except Exception as e:
        pass
