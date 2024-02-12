from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.keyboards.scenario_keyboard import get_menu_scenario


@dp.callback_query_handler(text="go_back_to_scenario")
async def scenario_handler(query: types.CallbackQuery, state: FSMContext):
    # try:
    #     await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    # except:
    #     pass

    await bot.send_message(
        query.message.chat.id,
        md.escape_md(
            f"Choose a scenario to practice your English"
            f" in various possible situations! 🗣️"),
        reply_markup=await get_menu_scenario())


@dp.message_handler(commands=["scenario"])
async def scenario_handler(message: types.Message, state: FSMContext):
    # try:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    # except:
    #     pass

    # await bot.send_message(message.chat.id, md.escape_md("Choose a scenario to practice your English"
    #                                                      f" in various possible situations! 🗣️"),
    #                        reply_markup=await get_menu_scenario())
    await bot.send_message(
        message.chat.id,
        md.escape_md(
            "We are working on this functionality and it will be ready soon! See you!"))
