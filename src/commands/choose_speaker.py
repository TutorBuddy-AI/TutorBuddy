from src.config import dp, bot
from src.utils.user import UserService

from aiogram import types, md


@dp.callback_query_handler(text="continue_bot")
async def continue_dialogue_with_bot(query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    except:
        pass

    await UserService().change_speaker(tg_id=str(query.message.chat.id), new_speaker="bot")

    await bot.send_message(query.message.chat.id, md.escape_md("Let's go!\n"
                                                               "Send me message below ⬇️"))

@dp.callback_query_handler(text="continue_nastya")
async def continue_dialogue_with_nastya(query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    except:
        pass

    await UserService().change_speaker(tg_id=str(query.message.chat.id), new_speaker="Anastasia")
    await bot.send_message(query.message.chat.id, md.escape_md("Let's go!\n"
                                                               "Send me message below ⬇️"))
