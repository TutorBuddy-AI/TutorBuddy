from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from src.commands.scenario.keyboard import menu_scenario_keyboard, menu_talk_show_keyboard
from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.keyboards.form_keyboard import get_choose_topic_keyboard
from src.states import FormTopic
from src.utils.user import UserService


@dp.message_handler(commands=["scenario"])
async def scenario_handler(message: types.Message, state: FSMContext):

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    await bot.send_message(message.chat.id, f"Choose scenario",
                           reply_markup=menu_scenario_keyboard)
