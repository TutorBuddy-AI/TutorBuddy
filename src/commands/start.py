import asyncio

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from src.commands.form_states import process_start_acquaintance
from src.config import dp, bot

from aiogram import types, md, Router

from src.filters import IsNotRegister
from src.texts import get_welcome_text
from src.utils.answer import AnswerRenderer
from src.texts.texts import get_person_welcome_text

start_router = Router(name=__name__)
start_router_person = Router(name=__name__ + "_person")

# @dp.message_handler(commands=["start"])
# async def menu_handler(message: types.Message):
#     await bot.send_message(message.chat.id,
#                            "Let's go!\nSend me message below ⬇️",
#                            parse_mode=ParseMode.HTML,
#                            reply_markup=types.ReplyKeyboardRemove())


@start_router.message(IsNotRegister(), CommandStart())
@start_router.message(IsNotRegister())
async def process_start_register_user(message: types.Message, state: FSMContext):
    """
    Function to explain bot idea for new users
    """
    welcome_text = get_welcome_text()
    caption_markup = AnswerRenderer.get_markup_caption_translation_standalone()

    await bot.send_photo(
        message.chat.id,
        caption=welcome_text,
        photo=FSInputFile("./files/tutorbuddy_welcome.png"),
        parse_mode=ParseMode.HTML,
        reply_markup=caption_markup
    )
    await asyncio.sleep(2)
    await process_start_acquaintance(message, state)


@start_router_person.message(IsNotRegister(), CommandStart())
@start_router_person.message(IsNotRegister())
async def process_start_register_user_person(message: types.Message, state: FSMContext):
    """
    Function to explain bot idea for new users
    """
    welcome_text = get_person_welcome_text()
    caption_markup = AnswerRenderer.get_markup_caption_translation_standalone()

    await bot.send_photo(
        message.chat.id,
        caption=welcome_text,
        photo=FSInputFile("./files/tutorbuddy_welcome.png"),
        parse_mode=ParseMode.HTML,
        reply_markup=caption_markup
    )
    await asyncio.sleep(2)
    await process_start_acquaintance(message, state)
