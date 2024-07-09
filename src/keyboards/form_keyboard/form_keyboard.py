from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.keyboards import get_go_back_inline_keyboard
from src.utils.answer import AnswerRenderer


async def get_choose_native_language_keyboard(for_user=False, is_caption=True) -> InlineKeyboardMarkup:
    rus = InlineKeyboardButton(text='Russian 🇷🇺', callback_data='native_RU')
    hindi = InlineKeyboardButton(text='Hindi 🇮🇳', callback_data='native_IN')

    persian = InlineKeyboardButton(text='Persian 🇮🇷', callback_data='native_IR')
    spanish = InlineKeyboardButton(text='Spanish 🇪🇸', callback_data='native_ESP')

    chinese = InlineKeyboardButton(text='Chinese 🇨🇳', callback_data='native_CN')
    german = InlineKeyboardButton(text='German 🇩🇪', callback_data='native_DE')

    french = InlineKeyboardButton(text='French 🇫🇷', callback_data='native_FR')
    other = InlineKeyboardButton(text='Other ✍️🏻', callback_data='other_language')

    if is_caption:
        translate_button = AnswerRenderer.get_button_caption_translation_standalone(for_user=for_user)
    else:
        translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=for_user)

    choose_native_language_inline_kb = InlineKeyboardMarkup(inline_keyboard=
                                                            [[rus, hindi], [persian, spanish], [chinese, german],
                                                             [french, other], [translate_button]])

    return choose_native_language_inline_kb


async def get_choose_goal_keyboard(is_caption=True) -> InlineKeyboardMarkup:
    business = InlineKeyboardButton(text='Business 💵', callback_data='goal_business')

    career = InlineKeyboardButton(text='Career 🪜', callback_data='goal_career')
    education = InlineKeyboardButton(text='Education 🎓', callback_data='goal_education')

    travel = InlineKeyboardButton(text='Travel ✈️', callback_data='goal_travel')
    relocate = InlineKeyboardButton(text='Move abroad 🌎', callback_data='goal_relocate')

    entertainment = InlineKeyboardButton(text='For fun 🎡', callback_data='goal_entertainment')
    love = InlineKeyboardButton(text='Love 💖️', callback_data='goal_love')

    friendship = InlineKeyboardButton(text='Friendship 👋🏻', callback_data='goal_friendship')
    network = InlineKeyboardButton(text='Network 🤝🏻', callback_data='goal_network')

    other = InlineKeyboardButton(text='Other✍️🏻', callback_data='other_goal')

    if is_caption:
        translate_button = AnswerRenderer.get_button_caption_translation_standalone()
    else:
        translate_button = AnswerRenderer.get_button_text_translation_standalone()

    choose_goal_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [business, education],
        [career, relocate],
        [travel, love],
        [friendship, network],
        [entertainment, other],
        [translate_button]
    ])

    return choose_goal_inline_kb


async def get_choose_english_level_keyboard(for_user=False, is_caption=True) -> InlineKeyboardMarkup:
    level_1 = InlineKeyboardButton(text='I can use simple words and basic phrases', callback_data='level_1')
    level_2 = InlineKeyboardButton(text='I can only have simple conversations',
                                   callback_data='level_2')

    level_3 = InlineKeyboardButton(text='I can talk about various subjects',
                                   callback_data='level_3')
    level_4 = InlineKeyboardButton(text='I express myself fluently in any situation', callback_data='level_4')

    if is_caption:
        translate_button = AnswerRenderer.get_button_caption_translation_standalone(for_user=for_user)
    else:
        translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=for_user)

    choose_english_level_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[level_1], [level_2], [level_3], [level_4], [translate_button]])

    return choose_english_level_inline_kb


async def get_choose_topic_keyboard(callback_query: CallbackQuery = None,
                                    for_user=False, is_caption=True) -> InlineKeyboardMarkup:
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
        psychology = InlineKeyboardButton(text='Psychology 🧠', callback_data='topic_psychology')
        business = InlineKeyboardButton(text='Business 💵', callback_data='topic_business')

        startups = InlineKeyboardButton(text='StartUps 🚀', callback_data='topic_startups')
        innovations = InlineKeyboardButton(text='Innovations 💡', callback_data='topic_innovations')

        fashion = InlineKeyboardButton(text='Fashion 🕶', callback_data='topic_fashion')
        health = InlineKeyboardButton(text='Health 🫁', callback_data='topic_health')

        other = InlineKeyboardButton(text='Other ✍️', callback_data='topic_other')

        done_button = InlineKeyboardButton(text='Accept ✅', callback_data='done')

        if is_caption:
            translate_button = AnswerRenderer.get_button_caption_translation_standalone(for_user=for_user)
        else:
            translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=for_user)

        choose_topic_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [psychology, business],
            [startups, innovations],
            [fashion, health],
            [other],
            [done_button],
            [translate_button]]
        )

    return choose_topic_inline_kb


async def get_choose_bot_keyboard(is_caption=True, bot_message: int | None = None,
                                  nastya_message: int | None = None) -> InlineKeyboardMarkup:
    if nastya_message:
        anastasia = InlineKeyboardButton(text='💁🏻‍♀️ Anastasia',
                                         callback_data=f'continue_nastya_{bot_message}_{nastya_message}')
    else:
        anastasia = InlineKeyboardButton(text='💁🏻‍♀️ Anastasia', callback_data='continue_nastya')

    if bot_message:
        tutor_buddy = InlineKeyboardButton(text='🤖 TutorBuddy',
                                           callback_data=f'continue_bot_{bot_message}_{nastya_message}')
    else:
        tutor_buddy = InlineKeyboardButton(text='🤖 TutorBuddy', callback_data='continue_bot')

    if is_caption:
        translate_button = AnswerRenderer.get_button_caption_translation_standalone()
    else:
        translate_button = AnswerRenderer.get_button_text_translation_standalone()
    choose_bot_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[tutor_buddy], [anastasia], [translate_button]])

    return choose_bot_inline_kb


async def get_keyboard_summary_choice(menu: bool) -> InlineKeyboardMarkup:
    if menu:
        accept = InlineKeyboardButton(text='Yes, sure! 🥳', callback_data='dispatch_summary_true')
        go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')
        translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=True)
        keyboard_summary_markup = InlineKeyboardMarkup(inline_keyboard=[[accept, go_back_btn], [translate_button]])
        return keyboard_summary_markup

    else:
        translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=True)
        accept = InlineKeyboardButton(text='Yes, sure! 🥳', callback_data='dispatch_summary_true')
        cancel = InlineKeyboardButton(text='No, thanks 😔', callback_data='dispatch_summary_false')
        keyboard_summary_markup = InlineKeyboardMarkup(inline_keyboard=[[accept, cancel], [translate_button]])
        return keyboard_summary_markup


async def get_keyboard_cancel_news_subs() -> InlineKeyboardMarkup:
    continue_btn = InlineKeyboardButton(text='Continue 🥳', callback_data='go_back')
    stop_subs_btn = InlineKeyboardButton(text='Stop 😔', callback_data='dispatch_summary_false')
    translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=True)
    keyboard_summary_markup = InlineKeyboardMarkup(inline_keyboard=[[translate_button], [continue_btn, stop_subs_btn]])
    return keyboard_summary_markup


async def get_keyboard_resume_news_subs() -> InlineKeyboardMarkup:
    accept = InlineKeyboardButton(text='Yes, sure! 🥳', callback_data='dispatch_summary_true')
    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')
    translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=True)
    keyboard_summary_markup = InlineKeyboardMarkup(inline_keyboard=[[translate_button], [accept, go_back_btn]])
    return keyboard_summary_markup
