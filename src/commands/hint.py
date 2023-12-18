from aiogram.dispatcher import FSMContext
from src.config import dp, bot

from aiogram import types, md
from utils.message_hint import MessageHintCreator, MessageHintService, MessageHintHelper


@dp.message_handler(commands=["hint"])
async def handle_get_hint(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageHintCreator(
        tg_id=str(message.from_user.id)
    ).create_communication_message_text()
    hint_info = await MessageHintHelper().group_message_hint_info(state_data, message, generated_text)
    await MessageHintService().create_message_hint(hint_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    # ToDo we should resend previous message with menu, so user could answer and use menu
