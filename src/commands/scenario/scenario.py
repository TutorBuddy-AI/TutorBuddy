from aiogram import types, md, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from src.config import dp, bot
from src.filters.is_not_register_filter import IsRegister
from src.keyboards.scenario_keyboard import get_menu_scenario
from src.utils.answer import AnswerRenderer

scenario_router = Router(name=__name__)


# @dp.callback_query_handler(text="go_back_to_scenario")
# async def scenario_handler(query: types.CallbackQuery, state: FSMContext):
#     # try:
#     #     await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
#     # except:
#     #     pass
#
#     await bot.send_photo(
#         query.message.chat.id,
#         photo=FSInputFile('./files/scenario.png'),
#         caption=
#             f"Choose a scenario to practice your English"
#             f" in various possible situations! 🗣️",
#         parse_mode=ParseMode.HTML,
#         reply_markup=await get_menu_scenario())


@scenario_router.message(IsRegister(), Command("scenario"))
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
        photo=FSInputFile('./files/scenario.png'),
        caption="We are working on this functionality and it will be ready soon! See you!",
        parse_mode=ParseMode.HTML,
        reply_markup=translate_markup
    )
