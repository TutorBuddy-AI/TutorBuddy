from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.config import dp, bot
from src.keyboards import get_cancel_keyboard_button, get_go_back_inline_keyboard
from src.keyboards.form_keyboard import get_choose_native_language_keyboard, get_choose_english_level_keyboard
from src.states import FormName, FormNativeLanguage, FormEnglishLevel
from src.utils.user import UserService
from src.texts.texts import get_incorrect_native_language_question, get_other_native_language_question


@dp.message_handler(commands=["editprofile"])
async def edit_profile_handler(message: types.Message):

    edit_profile_kb = InlineKeyboardMarkup(row_width=2)

    name = InlineKeyboardButton(text='Name', callback_data='change_name')
    topic = InlineKeyboardButton(text='Topics', callback_data='change_topic')

    native_language = InlineKeyboardButton(text='Native language', callback_data='change_native_language')
    english_level = InlineKeyboardButton(text='English Level', callback_data='change_english_level')

    user_topic = InlineKeyboardButton(text='Chosen topics', callback_data='get_user_topic')
    go_back = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    edit_profile_kb.row(name, topic).row(native_language, english_level).row(user_topic, go_back)

    await bot.send_photo(message.chat.id, photo=types.InputFile('./files/edit_profile.jpg'), caption=md.escape_md("What would you like to change?"),
                           reply_markup=edit_profile_kb)


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.callback_query_handler(lambda query: query.data == "change_name")
async def change_name_query_handler(query: CallbackQuery, state: FSMContext):
    user_info = await UserService().get_user_info(tg_id=str(query.message.chat.id))
    await state.set_state(FormName.new_name)

    await bot.send_message(query.message.chat.id, f"Current name: {user_info['name']}\n\n"
                                                  f"Write a new name ⬇",
                           reply_markup=await get_go_back_inline_keyboard())


@dp.message_handler(state=FormName.new_name)
async def changed_name_query_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    name = data["name"]

    await UserService().change_callname(tg_id=str(message.chat.id), new_callname=name)
    await state.finish()

    await bot.send_message(message.from_user.id, "The name has been successfully changed\n"
                                                 f"Current name: {name}",
                           reply_markup=await get_go_back_inline_keyboard())


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.callback_query_handler(lambda query: query.data == "change_native_language")
async def change_native_language_query_handler(query: CallbackQuery, state: FSMContext):
    user_info = await UserService().get_user_info(tg_id=str(query.message.chat.id))

    await state.set_state(FormNativeLanguage.new_native_language)

    await bot.send_message(query.message.chat.id, f"Current native language: {user_info['native_lang']}\n\n"
                                                  f"Choose the new native language",
                           reply_markup=await get_choose_native_language_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("native"), state=FormNativeLanguage.new_native_language)
async def changed_native_language_query_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(native_language=query.data.split("_")[1])

    state_data = await state.get_data()

    await UserService().change_native_language(tg_id=str(query.message.chat.id),
                                               new_native_language=state_data["native_language"])

    await bot.send_message(query.message.chat.id, "The native language has been successfully changed\n"
                                                  f"Current native language: {state_data['native_language']}",
                           reply_markup=await get_go_back_inline_keyboard())

    await state.finish()


@dp.callback_query_handler(lambda query: query.data == "other_language", state=FormNativeLanguage.new_native_language)
async def process_start_register_other_language(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.message.chat.id, get_other_native_language_question(),
        reply_markup = types.ReplyKeyboardRemove())
    await state.set_state(FormNativeLanguage.new_other_native_language)


@dp.message_handler(state=FormNativeLanguage.new_other_native_language)
async def process_other_language(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await bot.send_message(message.chat.id, get_incorrect_native_language_question())
    else:
        async with state.proxy() as data:
            data["native_language"]=message.text
        await UserService().change_native_language(
            tg_id=str(message.chat.id),
            new_native_language=message.text)
        await bot.send_message(message.chat.id, "The native language has been successfully changed\n"
                                                      f"Current native language: {message.text}",
                               reply_markup=await get_go_back_inline_keyboard())

        await state.finish()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.callback_query_handler(lambda query: query.data == "change_english_level")
async def change_english_level_query_handler(query: CallbackQuery, state: FSMContext):
    user_info = await UserService().get_user_info(tg_id=str(query.message.chat.id))

    await state.set_state(FormEnglishLevel.new_english_level)

    await bot.send_message(query.message.chat.id, md.escape_md(f"Current english level (where 1 is the worst level of"
                                                               f" English, and 4 is a good level of English):"
                                                               f" {user_info['english_level']}\n\n"
                                                               f"Choose your english leve"),
                           reply_markup=await get_choose_english_level_keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith("level"), state=FormEnglishLevel.new_english_level)
async def changed_english_level_query_handler(query: CallbackQuery, state: FSMContext):
    await state.update_data(english_level=query.data.split("_")[1])

    state_data = await state.get_data()

    await UserService().change_english_level(tg_id=str(query.message.chat.id),
                                             new_english_level=state_data["english_level"])

    await bot.send_message(query.message.chat.id, md.escape_md("The english level has been successfully changed!\n"
                                                               f"Current english level (where 1 is the worst level of"
                                                               f" English, and 4 is a good level of English):"
                                                               f" {state_data['english_level']}"),
                           reply_markup=await get_go_back_inline_keyboard())

    await state.finish()


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

@dp.callback_query_handler(lambda query: query.data == "get_user_topic")
async def change_get_user_topic_query_handler(query: CallbackQuery):
    user_info = await UserService().get_user_info(tg_id=str(query.message.chat.id))

    user_topic = ""

    for i, topic in enumerate(user_info['topic'].split(" ")):
        if topic != "":
            user_topic += f"{i + 1} -- {topic}\n"

    await bot.send_message(query.message.chat.id, md.escape_md(f"Current topic:\n"
                                                               f"{user_topic}"),
                           reply_markup=await get_go_back_inline_keyboard())
