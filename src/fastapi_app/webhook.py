from src.config import dp, bot
from src.commands.form_states import process_start_register_user, process_get_name
from src.filters import IsNotRegister
from src.states import Form
from src.utils.newsletter.newsletter import Newsletter
from aiogram import types

from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()


@app.post(f"/webhook")
async def receive_update(update: Dict, request: Request):
    update_obj = types.Update(**update)
    try:
        source = update_obj.message.get_args()
        context = dp.current_state(chat=update_obj.message.chat.id, user=update_obj.message.chat.id)
        await context.set_data({
            "ip_address": None,
            "source": source if source is not None else None,
            "tg_language": update_obj.message.from_user.language_code
        })
    except:
        pass
    finally:
        await dp.process_update(update_obj)

    return {"status_code": 200}



@app.get('/start_newsletter')
async def send_newsletter():
    try:
        await Newsletter().send_newsletter()
        return {'message': 'Newsletter sent'}
    except Exception as e:
        pass
