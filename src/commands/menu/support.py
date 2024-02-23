from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.keyboards import get_go_back_inline_keyboard
from src.states import FormSupport
from src.utils.answer import AnswerRenderer
from src.utils.generate.question_history.question_history import SupportHistory


@dp.message_handler(IsRegister(), commands=["support"])
async def support_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormSupport.message)

    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile('./files/support.png'),
        caption=md.escape_md("TutorBuddy team is always on duty!"
                             " 🦸🏻‍️🦸🏽‍️ What is the problem?"),
        reply_markup=await get_go_back_inline_keyboard())


@dp.message_handler(IsNotRegister(), commands=["support"])
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text=md.escape_md("Please, register first"), reply_markup=translate_markup)


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.message_handler(state=FormSupport.message)
async def support_query_handler(message: types.Message, state: FSMContext):

    await state.update_data(new_value=message.text)

    state_data = await state.get_data()

    await SupportHistory().add_questions(tg_id=str(message.chat.id), message=state_data['new_value'])

    await state.finish()

    await bot.send_message(message.chat.id, md.escape_md("Message sent successfully."
                                                         " The manager will definitely contact you. Thank you!"),
                           reply_markup=await get_go_back_inline_keyboard())
