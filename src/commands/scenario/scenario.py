from aiogram import types, md
from aiogram.fsm.context import FSMContext

from src.config import dp, bot
from src.filters.is_not_register_filter import IsRegister
from src.keyboards.scenario_keyboard import get_menu_scenario
from src.utils.answer import AnswerRenderer


@dp.callback_query_handler(text="go_back_to_scenario")
async def scenario_handler(query: types.CallbackQuery, state: FSMContext):
    # try:
    #     await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    # except:
    #     pass

    await bot.send_photo(
        query.message.chat.id,
        photo=types.InputFile('./files/scenario.png'),
        caption=md.escape_md(
            f"Choose a scenario to practice your English"
            f" in various possible situations! 🗣️"),
        reply_markup=await get_menu_scenario())


@dp.message_handler(IsRegister(), commands=["scenario"])
async def scenario_handler(message: types.Message, state: FSMContext):
    # try:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    # except:
    #     pass

    # await bot.send_photo(message.chat.id, photo=types.InputFile('./file/scenario.png'), caption=md.escape_md("Choose a scenario to practice your English"
    #                                                      f" in various possible situations! 🗣️"),
    #                        reply_markup=await get_menu_scenario())
    translate_markup = AnswerRenderer.get_markup_caption_translation_standalone(for_user=True)
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile('./files/scenario.png'),
        caption=md.escape_md(
            "We are working on this functionality and it will be ready soon! See you!"),
        reply_markup=translate_markup
    )
