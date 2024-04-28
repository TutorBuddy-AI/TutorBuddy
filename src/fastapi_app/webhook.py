import traceback

from aiogram.types import BotCommand

from commands.news_gallery import news_gallery_router
from commands.scenario.scenario import scenario_router
from src.commands.start import start_router, start_router_person
from src.config import config
from src.config import dp, bot
# from src.commands.form_states import process_start_register_user, process_get_name  # Magic Import - don't touch
from src.states import Form  # Magic Import - don't touch
from src.utils.newsletter.newsletter import Newsletter
from aiogram import types

import logging

from fastapi import FastAPI, Request
from typing import Dict

from src.commands.menu.go_back_to_chat import go_back_router
from src.commands.error import error_router
from src.commands.form_states import form_router
from src.commands.choose_speaker import choose_speaker_router
from src.commands.menu.edit_speaker import edit_speaker_router
from src.commands.menu.edit_topic import edit_topic_router
from src.commands.menu.mistakes import mistakes_router
from src.commands.menu.restart import restart_router
from src.commands.menu.support import support_router
from src.commands.menu.feedback import feedback_router
from src.commands.menu.summaries import summaries_router
from src.commands.cacncel_state import cancel_router
# from src.commands.scenario.scenario import sc
from src.commands.menu.edit_profile import edit_profile_router
from src.commands.text_communication import text_comm_router
from src.commands.audio_communication import audio_comm_router

app = FastAPI()

routers = []

if config.BOT_TYPE == "original":
    routers = [go_back_router, error_router, form_router, news_gallery_router,
               choose_speaker_router, edit_speaker_router,
               edit_topic_router, mistakes_router, restart_router, support_router, feedback_router,
               summaries_router, cancel_router, scenario_router, edit_profile_router, text_comm_router,
               audio_comm_router, start_router]
else:
    routers = [go_back_router, error_router, form_router, news_gallery_router, edit_speaker_router,
               edit_topic_router, mistakes_router, restart_router, support_router, feedback_router,
               summaries_router, cancel_router, scenario_router, edit_profile_router, text_comm_router,
               audio_comm_router, start_router_person]


dp.include_routers(*routers)


@app.on_event("startup")
async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
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

    bot_commands_1 = [
        BotCommand(command="/restart", description="⚙ Restart the bot"),
        BotCommand(command="/cancel", description="🔧Cancel current state (use if something went wrong)"),
        BotCommand(command="/summaries", description="📃 Summaries"),
        BotCommand(command="/scenario", description="🎬 Choose a scenario (soon)"),
        BotCommand(command="/changetopic", description="🔁 Change topic"),
        BotCommand(command="/editprofile", description="✏ Edit profile"),
    ]
    bot_commands_2 = [
        BotCommand(command="/summaries", description="📰 Summaries"),
        BotCommand(command="/all_mistakes", description="🔴 Show all my mistakes"),
        BotCommand(command="/support", description="👨💻 Contact support"),
        BotCommand(command="/feedback", description="💬 Leave feedback")
    ]
    if config.BOT_TYPE == "personal":
        bot_commands = bot_commands_1 + bot_commands_2
    else:
        bot_commands = (bot_commands_1
                        + [BotCommand(command="/persona", description="👥 Choose a persona to chat")]
                        + bot_commands_2)
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
            # source = update_obj.message.get_args()
            context = dp.fsm.resolve_context(
                bot=bot, chat_id=update_obj.message.chat.id, user_id=update_obj.message.from_user.id
            )
            data = await context.get_data()
            data["ip_address"] = None
            # data["source"] = source if source is not None else None
            data["source"] = None
            data["tg_language"] = update_obj.message.from_user.language_code
            await context.update_data(data)
        if update_obj.callback_query:
            context = dp.fsm.resolve_context(
                bot=bot, chat_id=update_obj.callback_query.from_user.id, user_id=update_obj.callback_query.from_user.id)
            data = await context.get_data()
            data["ip_address"] = None
            data["tg_language"] = update_obj.callback_query.from_user.language_code
            await context.update_data(data)
        await dp.feed_update(bot, update_obj)
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
        traceback.print_exc()
