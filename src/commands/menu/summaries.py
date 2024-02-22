from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.keyboards.form_keyboard.form_keyboard import get_keyboard_summary_choice

@dp.message_handler(commands=["summaries"])
async def summaries_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, md.escape_md("A quick reminder: news summaries is a format where I send you fresh global news and we share opinions on the topic 📃"))
    await bot.send_message(message.chat.id, md.escape_md("I am always willing to share some recent news summaries! Do you want me to start sending them from now on?"),
                            reply_markup=await get_keyboard_summary_choice(menu=True))


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#