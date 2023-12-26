from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_menu_scenario() -> InlineKeyboardMarkup:
    menu_scenario_inline_kb = InlineKeyboardMarkup(row_width=2)

    job_interview = InlineKeyboardButton(text="Job interview 💼", callback_data="job_interview_scenario")
    talk_show = InlineKeyboardButton(text="Talk show 🎙️", callback_data="talk_show_scenario")

    startup_pitch = InlineKeyboardButton(text="Startup pitch 💵", callback_data="startup_pitch_scenario")
    travel_agency = InlineKeyboardButton(text="Travel agency 🗺️", callback_data="travel_agency_scenario")

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    menu_scenario_inline_kb.row(job_interview, talk_show).row(startup_pitch, travel_agency).add(go_back_btn)

    return menu_scenario_inline_kb




