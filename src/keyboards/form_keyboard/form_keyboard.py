from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_choose_native_language_keyboard() -> InlineKeyboardMarkup:
    choose_native_language_inline_kb = InlineKeyboardMarkup(row_width=2)

    rus = InlineKeyboardButton(text='Russian 🇷🇺', callback_data='native_RU')
    hindi = InlineKeyboardButton(text='Hindi 🇮🇳', callback_data='native_IN')

    persian = InlineKeyboardButton(text='Persian 🇮🇷', callback_data='native_IR')
    spanish = InlineKeyboardButton(text='Spanish 🇪🇸', callback_data='native_ESP')

    chinese = InlineKeyboardButton(text='Chinese 🇨🇳', callback_data='native_CN')
    german = InlineKeyboardButton(text='German 🇩🇪', callback_data='native_DE')

    french = InlineKeyboardButton(text='French 🇫🇷', callback_data='native_FR')

    choose_native_language_inline_kb.row(rus, hindi).row(persian, spanish).row(chinese, german).row(french)

    return choose_native_language_inline_kb


async def get_choose_goal_keyboard() -> InlineKeyboardMarkup:
    choose_goal_inline_kb = InlineKeyboardMarkup(row_width=2)

    career = InlineKeyboardButton(text='Career 🪜', callback_data='goal_career')
    education = InlineKeyboardButton(text='Education 🎓', callback_data='goal_education')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='goal_travel')
    relocate = InlineKeyboardButton(text='Relocate 🌍️', callback_data='goal_relocate')

    culture = InlineKeyboardButton(text='Culture 🗽️', callback_data='goal_culture')

    choose_goal_inline_kb.row(career, education).row(travel, relocate).row(culture)

    return choose_goal_inline_kb


async def get_choose_english_level_keyboard() -> InlineKeyboardMarkup:

    choose_english_level_inline_kb = InlineKeyboardMarkup(row_width=1)

    level_1 = InlineKeyboardButton(text='I can use simple words and basic phrases', callback_data='level_1')
    level_2 = InlineKeyboardButton(text='I can have simple conversations about\n\n familiar topics',
                                   callback_data='level_2')

    level_3 = InlineKeyboardButton(text='I can communicate confidently\n\n on various subjects', callback_data='level_3')
    level_4 = InlineKeyboardButton(text='I express myself fluently in any situation', callback_data='level_4')

    choose_english_level_inline_kb.row(level_1).row(level_2).row(level_3).row(level_4)

    return choose_english_level_inline_kb


async def get_choose_topic_keyboard() -> InlineKeyboardMarkup:
    choose_topic_inline_kb = InlineKeyboardMarkup(row_width=2)

    book = InlineKeyboardButton(text='Books 📚', callback_data='topic_books')
    business = InlineKeyboardButton(text='Business 💵', callback_data='topic_business')

    movies = InlineKeyboardButton(text='Movies 🍿', callback_data='topic_movies')
    music = InlineKeyboardButton(text='Music 🎵', callback_data='topic_music')

    fashion = InlineKeyboardButton(text='Fashion 🕶️', callback_data='topic_fashion')
    art_and_design = InlineKeyboardButton(text='Art & Design 🎨', callback_data='topic_art_and_design')

    games = InlineKeyboardButton(text='Games 🕹️', callback_data='topic_games')
    innovations = InlineKeyboardButton(text='Innovations 💡', callback_data='topic_innovations')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='topic_travel')
    news = InlineKeyboardButton(text='News 📰', callback_data='topic_news')

    sports = InlineKeyboardButton(text='Sports ⚽️️', callback_data='topic_sports')
    career = InlineKeyboardButton(text='Career 💼', callback_data='topic_career')

    science = InlineKeyboardButton(text='Science 🧬', callback_data='topic_science')

    done_button = InlineKeyboardButton(text='Accept', callback_data='done')

    choose_topic_inline_kb.row(book, business).row(movies, music).row(fashion, art_and_design).row(games, innovations).\
        row(travel, news).row(sports, career).row(science).row(done_button)

    return choose_topic_inline_kb

async def get_choose_bot_keyboard() -> InlineKeyboardMarkup:
    choose_bot_inline_kb = InlineKeyboardMarkup(row_width=2)

    anastasia = InlineKeyboardButton(text='👩🏻‍🚀 Choose Anastasia', callback_data='soon....')
    nikita = InlineKeyboardButton(text='👨🏻‍💻 Choose Nikita', callback_data='soon....')

    tutor_buddy = InlineKeyboardButton(text='🤖 Proceed with TutorBuddy', callback_data='continue_bot')

    choose_bot_inline_kb.row(anastasia, nikita).row(tutor_buddy)

    return choose_bot_inline_kb
