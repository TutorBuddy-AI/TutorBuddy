from src.config import dp, bot

from aiogram import types, md


@dp.callback_query_handler(text="continue_bot")
async def continue_dialogue_with_bot(query: types.CallbackQuery):
    await bot.send_message(query.message.chat.id, md.escape_md("Let's go!\n"
                                                               "Send me message below ⬇️"))
