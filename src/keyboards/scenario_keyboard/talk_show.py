from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_choose_job_menu_talk_show_scenario() -> InlineKeyboardMarkup:
    choose_job_menu_scenario_inline_kb = InlineKeyboardMarkup(row_width=2)

    actor = InlineKeyboardButton(text="Actor 🎬", callback_data='talk_show_job_actor')
    singer = InlineKeyboardButton(text="Singer 🎤", callback_data='talk_show_job_singer')

    model = InlineKeyboardButton(text="Model 💄", callback_data='talk_show_job_model')
    blogger = InlineKeyboardButton(text="Blogger 📷", callback_data='talk_show_job_blogger')

    football_player = InlineKeyboardButton(text="Football player ⚽️", callback_data='talk_show_job_football-player')
    stand_up_comedian = InlineKeyboardButton(text="Stand up comedian 🎭", callback_data='talk_show_job_standup-comedian')

    fashion_designer = InlineKeyboardButton(text="Fashion designer 🧥", callback_data='talk_show_job_fashion-designer')
    ice_hockey_player = InlineKeyboardButton(text="Ice hockey player 🏒", callback_data='talk_show_job_ice_hockey-player')

    writer = InlineKeyboardButton(text="Writer 🖋️", callback_data='talk_show_job_writer')
    f1_driver = InlineKeyboardButton(text="F1 driver 🏎️", callback_data='talk_show_job_f1-driver')

    entrepreneur = InlineKeyboardButton(text="Entrepreneur 💼", callback_data='talk_show_job_entrepreneur')
    chef = InlineKeyboardButton(text="Chef 🍝", callback_data='talk_show_job_chef')

    other = InlineKeyboardButton(text="Other", callback_data='talk_show_job_other')
    go_back_to_scenario = InlineKeyboardButton(text="Go Back to Scenarios", callback_data='go_back_to_scenario')

    choose_job_menu_scenario_inline_kb.row(actor, singer).row(model, blogger).row(football_player, stand_up_comedian).row(fashion_designer, ice_hockey_player).row(writer, f1_driver).row(entrepreneur, chef).row(other, go_back_to_scenario)

    return choose_job_menu_scenario_inline_kb

async def get_end_menu_talk_show_scenario() -> InlineKeyboardMarkup:
    end_menu_talk_show_scenario_inline_kb = InlineKeyboardMarkup(row_width=2)

    restart = InlineKeyboardButton(text="Restart the scenario", callback_data="talk_show_scenario")
    choose_another_scenario = InlineKeyboardButton(text="Choose another scenario", callback_data="go_back_to_scenario")

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')
    give_feedback = InlineKeyboardButton(text='Give your feedback', callback_data='give_feedback')

    end_menu_talk_show_scenario_inline_kb.row(restart, choose_another_scenario).row(go_back_btn, give_feedback)

    return end_menu_talk_show_scenario_inline_kb
