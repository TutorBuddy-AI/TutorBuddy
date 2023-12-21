from aiogram.dispatcher import FSMContext
from src.config import dp, bot

from aiogram import types, md
from utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from utils.message_history_mistakes import MessageMistakesCreator


@dp.message_handler(commands=["mistakes"])
async def handle_get_mistakes(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageMistakesCreator(
        tg_id=str(message.from_user.id)
    ).create_communication_message_text()
    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(state_data, message, generated_text)
    await MessageMistakesService().create_mistakes(mistakes_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    # ToDo we should resend previous message with menu, so user could answer and use menu
