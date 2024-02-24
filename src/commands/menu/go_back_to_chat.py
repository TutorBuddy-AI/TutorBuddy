from src.config import dp, bot

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import md

from src.utils.answer import AnswerRenderer


@dp.callback_query_handler(text="go_back", state="*")
async def go_back_query_handler(query: CallbackQuery, state: FSMContext):

    await bot.send_message(query.message.chat.id, md.escape_md("Great!\nSend me message below ⬇"),
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

