from aiogram import md
from src.utils.payments.tariff_plans import get_tariff_plans


async def get_welcome_text():
    return md.text(
        "Hi! I'm **Tutor Buddy**, your personal English language practice tutor 💭\n\n"
        "I know how difficult it is to speak English without practice and a native speaker around.\n\n"
        "In order to feel confident in dialogues in a foreign language you need to get between 600 and 1,000 hours of "
        "practice. Talking to me every day will make it fun and rewarding.\n\n"
        "Let's get started! 🏄🏽‍♀️",
        sep='\n\n')

async def get_choose_bot_text():
    return md.escape_md(
        "You can continue talking to me or choose one of the other speaking partners. They are Tutor Buddy co-founder's"
        " digital twins, so you can get to know them through voice and visuals and discuss anything with them.\n\n"
        "👩🏻‍🚀 Anastasia is keen on entrepreneurship, fashion, movies and science\n\n"
        "👨🏻‍💻 Nikita is into music, innovations, sports and games\n\n"
        "Please notice that if you choose this option, another chat with a person will pop up."
    )

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
