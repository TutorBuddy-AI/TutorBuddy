from aiogram import types, md, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from src.config import bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.keyboards import get_go_back_inline_keyboard
from src.states import FormSupport
from src.utils.answer import AnswerRenderer
from src.utils.generate.question_history.question_history import SupportHistory

support_router = Router(name=__name__)


@support_router.message(IsRegister(), Command("support"))
async def support_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormSupport.message)

    await bot.send_photo(
        message.chat.id,
        photo=FSInputFile('./files/support.png'),
        caption="TutorBuddy team is always on duty!"
                " 🦸🏻‍️🦸🏽‍️ What is the problem?",
        parse_mode=ParseMode.HTML,
        reply_markup=await get_go_back_inline_keyboard())


@support_router.message(IsNotRegister(), Command("support"))
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text="Please, register first",
                           parse_mode=ParseMode.HTML, reply_markup=translate_markup)


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@support_router.message(FormSupport.message)
async def support_query_handler(message: types.Message, state: FSMContext):

    await state.update_data(new_value=message.text)

    state_data = await state.get_data()

    await SupportHistory().add_questions(tg_id=str(message.chat.id), message=state_data['new_value'])

    await state.clear()

    await bot.send_message(message.chat.id,
                           "Message sent successfully."
                           " The manager will definitely contact you. Thank you!",
                           parse_mode=ParseMode.HTML,
                           reply_markup=await get_go_back_inline_keyboard())
