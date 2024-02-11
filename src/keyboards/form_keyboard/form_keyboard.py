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
    other = InlineKeyboardButton(text='Other', callback_data='other_language')

    choose_native_language_inline_kb.row(rus, hindi).row(persian, spanish).row(chinese, german).row(french, other)

    return choose_native_language_inline_kb


async def get_choose_goal_keyboard() -> InlineKeyboardMarkup:
    choose_goal_inline_kb = InlineKeyboardMarkup(row_width=2)

    career = InlineKeyboardButton(text='Career 🪜', callback_data='goal_career')
    education = InlineKeyboardButton(text='Education 🎓', callback_data='goal_education')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='goal_travel')
    relocate = InlineKeyboardButton(text='Move abroad 🌎', callback_data='goal_relocate')

    culture = InlineKeyboardButton(text='Culture 🗽', callback_data='goal_culture')
    love = InlineKeyboardButton(text='Love 💖️', callback_data='goal_love')

    friendship = InlineKeyboardButton(text='Friendship 👋🏻', callback_data='goal_friendship')
    network = InlineKeyboardButton(text='Network 🤝🏻', callback_data='goal_network')

    other = InlineKeyboardButton(text='Other✍️🏻', callback_data='other_goal')

    (choose_goal_inline_kb
        .row(career, education).row(travel, relocate)
        .row(culture, love).row(friendship, network)
        .row(other)
     )

    return choose_goal_inline_kb


async def get_choose_english_level_keyboard() -> InlineKeyboardMarkup:

    choose_english_level_inline_kb = InlineKeyboardMarkup(row_width=1)

    level_1 = InlineKeyboardButton(text='I can use simple words and basic phrases', callback_data='level_1')
    level_2 = InlineKeyboardButton(text='I can only have simple conversations',
                                   callback_data='level_2')

    level_3 = InlineKeyboardButton(text='I can talk about various subjects',
                                   callback_data='level_3')
    level_4 = InlineKeyboardButton(text='I express myself fluently in any situation', callback_data='level_4')

    choose_english_level_inline_kb.row(level_1).row(level_2).row(level_3).row(level_4)

    return choose_english_level_inline_kb


async def get_choose_topic_keyboard() -> InlineKeyboardMarkup:
    choose_topic_inline_kb = InlineKeyboardMarkup(row_width=2)

    psychology = InlineKeyboardButton(text='Psychology 🧠', callback_data='topic_psychology')
    business = InlineKeyboardButton(text='Business 💵', callback_data='topic_business')

    science = InlineKeyboardButton(text='Science 🧬', callback_data='topic_science')
    innovations = InlineKeyboardButton(text='Innovations 💡', callback_data='topic_innovations')

    fashion = InlineKeyboardButton(text='Fashion 🕶️', callback_data='topic_fashion')
    art_and_design = InlineKeyboardButton(text='Art & Design 🎨', callback_data='topic_art_and_design')

    games = InlineKeyboardButton(text='Games 🕹️', callback_data='topic_games')
    music = InlineKeyboardButton(text='Music 🎵', callback_data='topic_music')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='topic_travel')
    book = InlineKeyboardButton(text='Books 📚', callback_data='topic_books')

    sports = InlineKeyboardButton(text='Sports ⚽️️', callback_data='topic_sports')
    health = InlineKeyboardButton(text='Health 🫁️', callback_data='topic_health')

    movies = InlineKeyboardButton(text='Movies 🍿', callback_data='topic_movies')
    other = InlineKeyboardButton(text='Other', callback_data='topic_other')

    # news = InlineKeyboardButton(text='News 📰', callback_data='topic_news')
    # career = InlineKeyboardButton(text='Career 💼', callback_data='topic_career')

    done_button = InlineKeyboardButton(text='Accept', callback_data='done')

    choose_topic_inline_kb.row(psychology, business).row(science, innovations).row(fashion, art_and_design).row(games, music).\
        row(travel, book).row(sports, health).row(movies, other).row(done_button)

    return choose_topic_inline_kb

async def get_choose_bot_keyboard() -> InlineKeyboardMarkup:
    choose_bot_inline_kb = InlineKeyboardMarkup(row_width=2)

    anastasia = InlineKeyboardButton(text='👩🏻‍🚀 Choose Anastasia', callback_data='continue_nastya')

    tutor_buddy = InlineKeyboardButton(text='🤖 Proceed with TutorBuddy', callback_data='continue_bot')

    choose_bot_inline_kb.row(anastasia, tutor_buddy)

    return choose_bot_inline_kb
