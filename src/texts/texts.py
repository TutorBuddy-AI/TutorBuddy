from aiogram import md
from src.utils.payments.tariff_plans import get_tariff_plans


def get_welcome_text_before_start():
    return md.text(
        "Hi! This is your personal Tutor Buddy and I will help you to improve your English.\n\n"
        "By practicing English everyday with me, you will be able to:\n\n"
        "🚀 work or study abroad\n"
        "⚡️ excel at a job interview\n"
        "🌟 ace your exams\n"
        "have everyday conversations and build your confidence!")


def get_welcome_text():
    return md.escape_md(
        f"Hi! I'mTutor Buddy, your personal English language practice tutor 💭\n\n"
        "I know how difficult it is to speak English without practice and a native speaker around.\n\n"
        "In order to feel confident in dialogues in a foreign language you need to get between 600 and 1,000 hours of "
        "practice. Talking to me every day will make it fun and rewarding.\n\n"
        "Let's get started! 🏄🏽‍♀️")


def get_lets_know_each_other():
    return md.text(
        "Let's get to know each other first"
    )


def get_choose_bot_text():
    return md.escape_md(
        "You can continue talking to me or choose one of the other speaking partners. They are Tutor Buddy co-founder's"
        " digital twins, so you can get to know them through voice and visuals and discuss anything with them.\n\n"
        "👩🏻‍🚀 Anastasia is keen on entrepreneurship, fashion, movies and science\n\n"
        "Please notice that if you choose this option, another chat with a person will pop up."
    )


def get_other_native_language_question():
    return md.escape_md(
        "What is your native language? Write only its name, for example, 'Japanese'"
    )


def get_incorrect_native_language_question():
    return md.escape_md(
        "The name of the language looks incorrect. Please use only English characters in the name of the language.\n"
        "Please, tell me the other name of your native language"
    )


def get_other_goal():
    return md.escape_md(f"Please describe the reason why you want to practice English?")


def get_chose_some_topics():
    return md.escape_md(
        "Choose some appealing topics (one or more). "
        "It will help us to have interesting conversations and I will also share some relevant news! 🤩"
    )


def get_chose_some_more_topics():
    return md.text(
        "Please, choose 1+ topics"
    )


def get_other_topics():
    return md.escape_md(
        "Please list other topics that interest you, separated by commas. "
        "Example: '3d printing, knitting'"
    )


def get_choose_buddy_text():
    return md.escape_md(
        "To have even more fun practicing English, "
        "you can talk to Anastasia, a digital twin of the TutorBuddy's founder! 💁🏻‍♀️\n\n"
        "She can be your speaking partner, "
        "so you will get to know her through voice and visuals. "
        "Anastasia is open to share opinions and debate on various topics 💬\n\n"
        "By the way, another digital twins will be available soon! "
        "🌟 You can switch personas later using menu."
    )


def get_choice_is_done():
    return md.escape_md("Great! Whenever you want to switch between personas, go to Menu and choose the one!")


def get_greeting_anastasia():
    return ("I am Anastasia, nice to meet you! "
    "I am an entrepreneur and the TutorBuddy's founder! "
    "I'm interested in technology, fashion, movies, innovations and science. "
    "I am a digital twin, but you can")


def get_start_talk(is_bot: bool, name: str):
    prefix = f"Hi, {name}! " if is_bot else ""
    return (
            prefix + "The best way to practice spoken English is to speak! "
            "Go ahead and send me a voice message or text me. "
            "Tell me, how is your day going?")




# def get_models_text():
#     return md.text(
#         md.text(
#             md.text('Choose the model you want to work with:')
#         ),
#         md.text(
#             md.text(
#                 md.text(md.bold('ChatGPT 3'), md.escape_md(
#                     '.'), md.bold('5 Turbo'), sep=''),
#                 md.escape_md(md.text(
#                     'One of the most powerful models currently from OpenAI, which is a language model with billions of parameters that is trained on huge amounts of text data.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: more than 60 languages.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.text(md.bold('ChatGPT 3'), md.escape_md(
#                     '.'), md.bold('5 Turbo 0301'), sep=''),
#                 md.escape_md(md.text(
#                     'Improved version of ChatGPT 3.5. Improved context understanding and performance.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: more than 60 languages.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('ChatGPT 4')),
#                 md.escape_md(md.text(
#                     'The most "smart" and "human" model from OpenAI at the moment.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: more than 60 languages.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('ChatGPT 4 32k')),
#                 md.escape_md(md.text(
#                     'An improved model that differs mainly in the length of responses, which is noticeably longer than ChatGPT 4.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: more than 60 languages.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Google Chat Bison Palm2')),
#                 md.escape_md(md.text(
#                     'One of the most powerful models from Google at the moment is PaLM2.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language Support: 🇺🇸English, 🇪🇸Spanish, 🇰🇷Korean, 🇮🇳Hindi, 🇨🇳Chinese.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Meta Llama2')),
#                 md.escape_md(md.text(
#                     'LLaMA (Large Language Model Meta AI) is Meta"s NLP model with billions of parameters, trained in 20 languages.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: 🇺🇸English, 🇪🇸Spanish, etc.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Falcon 7b')),
#                 md.escape_md(md.text(
#                     'This is the first large-language model from the Institute of Technological Innovation in the UAE and the Middle East, trained on one trillion tokens.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: 🇺🇸English, 🇫🇷French.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Falcon 40b')),
#                 md.escape_md(md.text(
#                     'An improved model that supports more languages, is faster, and understands context better.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language Support: 🇺🇸English, 🇩🇪German, 🇪🇸Spanish, 🇫🇷French.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('DALLE 2')),
#                 md.escape_md(md.text(
#                     'One of the strongest generative models to date from OpenAI that generates images.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language support: more than 100 languages'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Stability AI')),
#                 md.escape_md(md.text(
#                     'The "most advanced" text-to-image model from startup Stability AI with brighter, more accurate colors and better contrast.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md('Language support: 🇺🇸English.'))
#             ),
#             sep='\n'
#         ),
#
#         md.text(
#             md.text(
#                 md.bold(md.escape_md('Unity Muse Beta')),
#                 md.escape_md(md.text(
#                     'Beta version of Unity"s AI Chat, which knows everything about Unity development.')),
#                 sep='\n'),
#             md.text(
#                 md.text(md.escape_md(
#                     'Language Support: 🇺🇸English'))
#             ),
#             sep='\n'
#         ),
#         sep='\n\n'
#     )
