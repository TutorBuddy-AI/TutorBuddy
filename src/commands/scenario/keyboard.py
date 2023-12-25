from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

menu_talk_show_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Actor", callback_data="job_actor"),
        InlineKeyboardButton(text="Singer", callback_data="job_singer"),
        InlineKeyboardButton(text="Model", callback_data="job_model"),
        InlineKeyboardButton(text="Blogger", callback_data="job_blogger"),
        InlineKeyboardButton(text="Football Player", callback_data="job_football_player"),
    ],
    [
        InlineKeyboardButton(text="Stand-up Comedian", callback_data="job_standup_comedian"),
        InlineKeyboardButton(text="Fashion Designer", callback_data="job_fashion_designer"),
        InlineKeyboardButton(text="Ice Hockey Player", callback_data="job_ice_hockey_player"),
        InlineKeyboardButton(text="Writer", callback_data="job_writer"),
        InlineKeyboardButton(text="F1 Driver", callback_data="job_f1_driver"),
    ],
    [
        InlineKeyboardButton(text="Entrepreneur", callback_data="job_entrepreneur"),
        InlineKeyboardButton(text="Chef", callback_data="job_chef"),
        InlineKeyboardButton(text="Other", callback_data="job_other"),
        InlineKeyboardButton(text="Go Back to Scenarios", callback_data="go_back_to_scenarios"),
    ],
])

menu_scenario_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        InlineKeyboardButton(text="Talk show", callback_data="talk_show_scenario")
    ])


async def get_choose_native_language_keyboard() -> InlineKeyboardMarkup:
    choose_native_language_inline_kb = InlineKeyboardMarkup(row_width=2)

    actor = InlineKeyboardButton(text="Actor", callback_data="job_actor"),
    singer = InlineKeyboardButton(text="Singer", callback_data="job_singer"),
    model = InlineKeyboardButton(text="Model", callback_data="job_model"),
    blogger = InlineKeyboardButton(text="Blogger", callback_data="job_blogger"),
    football_player = InlineKeyboardButton(text="Football Player", callback_data="job_football_player"),
    stand_up_comedian = InlineKeyboardButton(text="Stand-up Comedian", callback_data="job_standup_comedian"),
    fashion_designer = InlineKeyboardButton(text="Fashion Designer", callback_data="job_fashion_designer"),
    ice_hockey_player = InlineKeyboardButton(text="Ice Hockey Player", callback_data="job_ice_hockey_player"),
    writer = InlineKeyboardButton(text="Writer", callback_data="job_writer"),
    f1_driver = InlineKeyboardButton(text="F1 Driver", callback_data="job_f1_driver"),
    entrepreneur=InlineKeyboardButton(text="Entrepreneur", callback_data="job_entrepreneur"),
    chef = InlineKeyboardButton(text="Chef", callback_data="job_chef"),
    Other = InlineKeyboardButton(text="Other", callback_data="job_other"),
    go_back_to_scenarios = InlineKeyboardButton(text="Go Back to Scenarios", callback_data="go_back_to_scenarios")

    # choose_native_language_inline_kb.row(rus, hindi).row(persian, spanish).row(chinese, german).row(french)
    #
    # return choose_native_language_inline_kb
    return "hello"
