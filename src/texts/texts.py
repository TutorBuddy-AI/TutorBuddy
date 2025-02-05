from aiogram import md
from aiogram.utils.markdown import bold
from emoji import emojize
from src.utils.payments.tariff_plans import get_tariff_plans


def get_welcome_text_before_start():
    return (
        "Hi! This is your personal TutorBuddy and I will help you to improve your English.\n\n"
        "By practicing English everyday with me, you will be able to:\n\n"
        "🚀 work or study abroad\n"
        "⚡️ excel at a job interview\n"
        "🌟 ace your exams\n"
        "have everyday conversations and build your confidence!")


def get_welcome_text():
    return (
        f"Привет! Я TutorBuddy AI, твой цифровой тьютор для практики английского 😊\n\n"
        "Знаю, что свободно говорить сложно, для этого нужно много времени (600 - 1000+ часов! 😱).\n\n" 
	"Хочу общаться с тобой на интересные темы и быть твоим умным другом, который учит и корректирует 24/7.\n\n" 
	"Давай знакомиться! 🏄🏽‍♀️")


def get_person_welcome_text():
    return (
        f"Hello! With this Telegram bot, you now have access to a world of immersive English practice, "
        f"right at your fingertips 24/7. "
        f"We'll work together to take your language skills to new heights through interactive activities, "
        f"real-world scenarios, and lots of conversation practice. \n\n"
        f"So let's get started! I'm just a message away whenever you need practice, "
        f"feedback or simply someone to chat with in English 💬")


def get_lets_know_each_other():
    return (
        "Let's get to know each other first"
    )


def get_choose_bot_text():
    return (
        "You can continue talking to me or choose one of the other speaking partners. They are Tutor Buddy co-founder's"
        " digital twins, so you can get to know them through voice and visuals and discuss anything with them.\n\n"
        "👩🏻‍🚀 Anastasia is keen on entrepreneurship, fashion, movies and science\n\n"
        "Please notice that if you choose this option, another chat with a person will pop up."
    )


def get_other_native_language_question():
    return (
        "What is your native language? Write only its name, for example, 'Japanese'"
    )


def get_incorrect_native_language_question():
    return (
        "The name of the language looks incorrect. Please use only English characters in the name of the language.\n"
        "Please, tell me the other name of your native language"
    )


def get_other_goal():
    return (f"Please describe the reason why you want to practice English?")


def get_chose_some_topics():
    return (
        "Выбери несколько интересных тебе тем и мы сможем:\n"
	"⚡️ вести реально интересные беседы\n"
	"⚡️ обсуждать свежие новости мировых сми"

    )


def get_chose_some_more_topics():
    return (
        "Please, choose 1+ topics"
    )


def get_other_topics():
    return (
        "Please list other topics that interest you, separated by commas. "
        "Example: '3d printing, knitting'"
    )


def get_choose_buddy_text():
    return (
        "To have even more fun practicing English, "
        "you can talk to Anastasia, a digital twin of the TutorBuddy's founder! 💁🏻‍♀️\n\n"
        "She can be your speaking partner, "
        "so you will get to know her through voice and visuals. "
        "Anastasia is open to share opinions and debate on various topics 💬\n\n"
        "By the way, another digital twins will be available soon! "
        "🌟 You can switch personas later using menu."
    )


def get_choice_is_done():
    return ("Отлично! Когда захочешь переключиться между персонами, зайдите в Меню и выберите нужную!")


def get_greeting_anastasia():
    return (
        "I am Anastasia, nice to meet you! "
        "I am an entrepreneur and the TutorBuddy's founder! "
        "I'm interested in technology, fashion, movies, innovations and science. "
        "I am a digital twin, but you can")


def get_start_talk(is_bot: bool, name: str):
    prefix = f"Hi, {name}! " if is_bot else ""
    return prefix + get_check_text()


def get_check_text():
    return (
        "The best way to practice spoken English is to speak! "
        "Go ahead and send me a voice message or text me. "
        "Tell me, how is your day going?")


def get_start_person_talk(person_id: str, person_name: str):
    match person_id:
        case "Victoria":
            persons_text = (
                f"My name is Victoria. "
                f"I’m an English teacher for adults. "
                f"I hold a degree in English language and linguistics and utilize a variety of teaching approaches. "
                f"I can help you with improving your pronunciation, speaking, "
                f"and I can also be your perfect English friend and mentor, "
                f"ensuring your English improves significantly!")
        case "Katya":
            persons_text = (
                f"My name is Katya, and I'm here to help you excel in English. "
                f"Whether you're preparing for interviews, gearing up for a move to an English-speaking country, "
                f"or adjusting to a new environment, I've got you covered."
                "\n\n"
                "I'm not your average chatbot – you'll get to know me through visuals and voice interactions. "
                "Think of me as your conversation partner, ready to engage in friendly debates! "
                "This personal touch will truly enhance your English fluency "
                "and give you the confidence you need to succeed.")
        case _:
            persons_text = (
                f"My name is {person_name} and I'm a certified English teacher. "
                "I specialize in teaching Business English to tech professionals, "
                "IT and digital experts and entrepreneurs."
                "\n\n"
                "I'm not just another chatbot — you'll get to know me through visuals and voice interactions. "
                "I'm here as your speaking partner, ready to discuss ideas, share opinions, "
                "and even have friendly debates! "
                "This personal touch will truly level up your English fluency.")
    return persons_text


def get_meet_bot_text():
    return ("I am TutorBuddy, that one English-speaking friend, "
            "who is always there to help you sharpen your language skills. "
            "My range of interest is quite wide and I hope we’ll find a lot in common "
            "By the way, meet Anastasia, a digital twin of the TutorBuddy's founder! ")


def get_meet_bot_message():
    return (
        "Я - TutorBuddy AI, тот самый англоговорящий друг, который всегда готов помочь практиковать английский )\n" 
	"Надеюсь, что мы найдем много общего 😉\n\n" 
	"Кстати, познакомься с  Анастасией, DigitalTwin основательницы TutorBuddy! 💁🏻‍♀️"
    )


def get_meet_nastya_text(name):
    return (f"Привет, {name}, меня зовут Anastasia Andrizh, ИТ-предприниматель и продакт."
	    f"Я занимаюсь бизнесом с 19 лет. Сейчас создаю этот стартап, CoPilot TutorBuddy AI, и практикую английский вместе со всеми пользователями."
	    f"Я также могу общаться с тобой на разные темы, можно узнать меня через голос и визуал. Больше всего мне нравятся темы инноваций, стартапов и моды."
	    f"Я буду рада поделиться своим мнением, услышать твое и подискутировать вместе по разным топикам ")


def get_meet_nastya_message(name):
    return (get_meet_nastya_text(name) + "💬")


def get_first_summary(name):
    return f"Hi, {name}! I want to keep you updated " \
           f"of what is going on in the world, so " \
           f"you can dive into context and expand " \
           f"your vocabulary 🌎 I will send you " \
           f"*fresh news summaries* from international sources on the topics of your choice, so we can discuss them and share opinions.\n" \
           f"Later on I will also share summaries of videos and podcasts 🎧 Are you interested? 😎"


def get_pin_message(translate: bool = False):
    if translate:
        return 'Кстати, чтобы не потерять наш чат, предлагаю закрепить его в ленте 😉 Это можно сделать просто нажав на него в ленте чатов и выбрав "Закрепить" 📌'
    else:
        return "By the way, I'm afraid you can lose our chat and your opportunity to become a fluent speaker. Make me your first priority! All you need to do is to open your chat list, long press our chat and tap 'pin', so you will see it on top! 📌"


def get_bot_waiting_message(speaker: str) -> str:
    return f"⏳ {speaker} is thinking … Please wait"


def get_translation_text(lang):
    return f"\n\n{emojize(':' + lang + ':', language='alias')} Translated text:\n"

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
