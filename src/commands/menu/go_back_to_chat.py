from src.config import bot

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import md, Router

from src.utils.answer import AnswerRenderer

go_back_router = Router(name=__name__)


@go_back_router.callback_query(F.text == "go_back", F.state == "*")
async def go_back_query_handler(query: CallbackQuery, state: FSMContext):

    await bot.send_message(query.message.chat.id, md.escape_md("Great!\nSend me message below ⬇"),
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()

