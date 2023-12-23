from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.states import FormSupport
from src.utils.generate.question_history.question_history import SupportHistory


@dp.message_handler(commands=["support"])
async def support_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormSupport.message)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    await bot.send_message(message.chat.id, md.escape_md("TutorBuddy team is always on duty!"
                                                         " 🦸🏻‍️🦸🏽‍️ What is the problem?"),
                           reply_markup=await get_go_back_inline_keyboard())


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.message_handler(state=FormSupport.message)
async def support_query_handler(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    await state.update_data(new_value=message.text)

    state_data = await state.get_data()

    await SupportHistory().add_questions(tg_id=str(message.chat.id), message=state_data['new_value'])

    await state.finish()

    await bot.send_message(message.chat.id, md.escape_md("Message sent successfully."
                                                         " The manager will definitely contact you. Thank you!"),
                           reply_markup=await get_go_back_inline_keyboard())
