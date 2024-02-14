from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.utils.answer import AnswerRenderer


async def get_choose_native_language_keyboard(for_user=False) -> InlineKeyboardMarkup:
    choose_native_language_inline_kb = InlineKeyboardMarkup(row_width=2)

    rus = InlineKeyboardButton(text='Russian 🇷🇺', callback_data='native_RU')
    hindi = InlineKeyboardButton(text='Hindi 🇮🇳', callback_data='native_IN')

    persian = InlineKeyboardButton(text='Persian 🇮🇷', callback_data='native_IR')
    spanish = InlineKeyboardButton(text='Spanish 🇪🇸', callback_data='native_ESP')

    chinese = InlineKeyboardButton(text='Chinese 🇨🇳', callback_data='native_CN')
    german = InlineKeyboardButton(text='German 🇩🇪', callback_data='native_DE')

    french = InlineKeyboardButton(text='French 🇫🇷', callback_data='native_FR')
    other = InlineKeyboardButton(text='Other', callback_data='other_language')

    choose_native_language_inline_kb.row(rus, hindi).row(persian, spanish).row(chinese, german).row(french, other).row(
            AnswerRenderer.get_button_text_translation_standalone(for_user=for_user))

    return choose_native_language_inline_kb


async def get_choose_goal_keyboard() -> InlineKeyboardMarkup:
    choose_goal_inline_kb = InlineKeyboardMarkup(row_width=2)
    business = InlineKeyboardButton(text='Business 💵', callback_data='goal_business')

    career = InlineKeyboardButton(text='Career 🪜', callback_data='goal_career')
    education = InlineKeyboardButton(text='Education 🎓', callback_data='goal_education')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='goal_travel')
    relocate = InlineKeyboardButton(text='Move abroad 🌎', callback_data='goal_relocate')

    entertainment = InlineKeyboardButton(text='For fun 🗽', callback_data='goal_entertainment')
    love = InlineKeyboardButton(text='Love 💖️', callback_data='goal_love')

    friendship = InlineKeyboardButton(text='Friendship 👋🏻', callback_data='goal_friendship')
    network = InlineKeyboardButton(text='Network 🤝🏻', callback_data='goal_network')

    other = InlineKeyboardButton(text='Other✍️🏻', callback_data='other_goal')

    (choose_goal_inline_kb
     .row(business, education)
     .row(career, relocate).row(travel, love)
     .row(friendship, network)
     .row(entertainment, other)
     .row(AnswerRenderer.get_button_text_translation_standalone())
     )

    return choose_goal_inline_kb


async def get_choose_english_level_keyboard(for_user=False) -> InlineKeyboardMarkup:
    choose_english_level_inline_kb = InlineKeyboardMarkup(row_width=1)

    level_1 = InlineKeyboardButton(text='I can use simple words and basic phrases', callback_data='level_1')
    level_2 = InlineKeyboardButton(text='I can only have simple conversations',
                                   callback_data='level_2')

    level_3 = InlineKeyboardButton(text='I can talk about various subjects',
                                   callback_data='level_3')
    level_4 = InlineKeyboardButton(text='I express myself fluently in any situation', callback_data='level_4')

    choose_english_level_inline_kb.row(level_1).row(level_2).row(level_3).row(level_4).row(
        AnswerRenderer.get_button_text_translation_standalone(for_user=for_user))

    return choose_english_level_inline_kb


async def get_choose_topic_keyboard(callback_query: CallbackQuery = None, for_user=False) -> InlineKeyboardMarkup:
    if callback_query:
        choose_topic_inline_kb = callback_query.message.reply_markup

        for row in choose_topic_inline_kb.inline_keyboard:
            for button in row:
                if button.callback_data == callback_query.data:
                    if button.text.startswith("✅ "):
                        button.text = button.text.replace("✅ ", "")
                    else:
                        button.text = "✅ " + button.text
                    break
    else:
        choose_topic_inline_kb = InlineKeyboardMarkup(row_width=2)

        psychology = InlineKeyboardButton(text='Psychology 🧠', callback_data='topic_psychology')
        business = InlineKeyboardButton(text='Business 💵', callback_data='topic_business')

        startups = InlineKeyboardButton(text='StartUps 🚀', callback_data='topic_startups')
        innovations = InlineKeyboardButton(text='Innovations 💡', callback_data='topic_innovations')

        fashion = InlineKeyboardButton(text='Fashion 🕶', callback_data='topic_fashion')
        art_and_design = InlineKeyboardButton(text='Art & Design 🎨', callback_data='topic_art_and_design')

        games = InlineKeyboardButton(text='Games 🕹', callback_data='topic_games')
        science = InlineKeyboardButton(text='Science 🧬', callback_data='topic_science')

        travel = InlineKeyboardButton(text='Travel ✈️', callback_data='topic_travel')
        book = InlineKeyboardButton(text='Books 📚', callback_data='topic_books')

        sports = InlineKeyboardButton(text='Sports ⚽️', callback_data='topic_sports')
        health = InlineKeyboardButton(text='Health 🫁', callback_data='topic_health')

        movies = InlineKeyboardButton(text='Movies 🍿', callback_data='topic_movies')
        other = InlineKeyboardButton(text='Other ✍️🗒', callback_data='topic_other')

        # news = InlineKeyboardButton(text='News 📰', callback_data='topic_news')
        # career = InlineKeyboardButton(text='Career 💼', callback_data='topic_career')

        done_button = InlineKeyboardButton(text='Accept ✅', callback_data='done')

        choose_topic_inline_kb.add(
            psychology, business,
            startups, innovations,
            fashion, art_and_design,
            games, science,
            travel, book,
            sports, health,
            movies, other
        )
        choose_topic_inline_kb.row(done_button).row(
            AnswerRenderer.get_button_text_translation_standalone(for_user=for_user))

    return choose_topic_inline_kb


async def get_choose_bot_keyboard() -> InlineKeyboardMarkup:
    choose_bot_inline_kb = InlineKeyboardMarkup()

    anastasia = InlineKeyboardButton(text='👩🏻‍🚀 Choose Anastasia', callback_data='continue_nastya')

    tutor_buddy = InlineKeyboardButton(text='🤖 Proceed with TutorBuddy', callback_data='continue_bot')

    choose_bot_inline_kb.row(anastasia).row(tutor_buddy).row(
        AnswerRenderer.get_button_caption_translation_standalone())

    return choose_bot_inline_kb
