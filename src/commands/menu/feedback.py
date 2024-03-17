from aiogram import types, md, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from src.config import bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.keyboards import get_go_back_inline_keyboard
from src.states import FormFeedback
from src.utils.answer import AnswerRenderer
from src.utils.generate.feedback_loop import FeedbackHistory

feedback_router = Router(name=__name__)


@feedback_router.callback_query(F.data == "give_feedback")
async def feedback_handler(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(FormFeedback.message)

    await bot.send_photo(query.message.chat.id, photo=FSInputFile('./files/feedback.jpg'),
                         caption=("TutorBuddy team is always glad to hear your feedback!"
                                              " Tell us what do you like or dislike about this bot and"
                                              " how can we improve it?\n"
                                              "Please, send text message"),
                         reply_markup=await get_go_back_inline_keyboard())


@feedback_router.message(IsRegister(), Command("feedback"))
async def feedback_handler(message: types.Message, state: FSMContext):
    await state.set_state(FormFeedback.message)

    await bot.send_photo(message.chat.id, photo=FSInputFile('./files/feedback.jpg'),
                         caption="TutorBuddy team is always glad to hear your feedback!"
                                 " Tell us what do you like or dislike about this bot and"
                                 " how can we improve it?\n"
                                 "Please, send text message",
                         parse_mode=ParseMode.HTML,
                         reply_markup=await get_go_back_inline_keyboard())


@feedback_router.message(IsNotRegister(), Command("feedback"))
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, "Please, register first", parse_mode=ParseMode.HTML,
                           reply_markup=translate_markup)


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@feedback_router.message(FormFeedback.message)
async def feedback_query_handler(message: types.Message, state: FSMContext):

    await state.update_data(new_value=message.text)

    state_data = await state.get_data()

    await FeedbackHistory().add_feedback(tg_id=str(message.chat.id), message=state_data['new_value'])
    await state.clear()

    url_telegram = f"https://t.me/{message.chat.username}"
    message_group = f"<b>From 💬 feedback</b>\n" \
                    f"<b>User:</b> {url_telegram}\n" \
                    f"<b>Message:</b> <i>{message.text}</i>"

    await bot.send_message('-1001938775399', message_group, parse_mode=types.ParseMode.HTML)

    await bot.send_message(message.chat.id,
                           text="Message sent successfully. Thank you!",
                           parse_mode=ParseMode.HTML,
                           reply_markup=await get_go_back_inline_keyboard())
