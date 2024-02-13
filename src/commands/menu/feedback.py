from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.states import FormFeedback
from src.utils.generate.feedback_loop import FeedbackHistory


@dp.callback_query_handler(text="give_feedback")
async def feedback_handler(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(FormFeedback.message)

    await bot.send_photo(query.message.chat.id, photo=types.InputFile('./files/feedback.jpg'), caption=md.escape_md("TutorBuddy team is always glad to hear your feedback!"
                                                               " Tell us what do you like or dislike about this bot and"
                                                               " how can we improve it?"),
                           reply_markup=await get_go_back_inline_keyboard())


@dp.message_handler(commands=["feedback"])
async def feedback_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormFeedback.message)

    await bot.send_photo(message.chat.id,photo=types.InputFile('./files/feedback.jpg'), caption=md.escape_md("TutorBuddy team is always glad to hear your feedback!"
                                                         " Tell us what do you like or dislike about this bot and"
                                                         " how can we improve it?"),
                           reply_markup=await get_go_back_inline_keyboard())


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.message_handler(state=FormFeedback.message)
async def feedback_query_handler(message: types.Message, state: FSMContext):

    await state.update_data(new_value=message.text)

    state_data = await state.get_data()

    await FeedbackHistory().add_feedback(tg_id=str(message.chat.id), message=state_data['new_value'])
    await state.finish()

    await bot.send_message(message.chat.id, md.escape_md("Message sent successfully. Thank you!"),
                           reply_markup=await get_go_back_inline_keyboard())
