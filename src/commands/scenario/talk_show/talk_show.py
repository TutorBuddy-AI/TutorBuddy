import asyncio

from aiogram.fsm.context import FSMContext

from src.config import dp, bot
from src.states.scenario import TalkShowForm
from aiogram import types, md
from src.keyboards.scenario_keyboard import get_choose_job_menu_talk_show_scenario, get_end_menu_talk_show_scenario
from src.utils.generate.communication import ScenarioTalkShowGenerate
from src.commands.scenario.prompts import TalkShowPrompt


async def _genarate_text(tg_id: str, prompt: str, job: str) -> str:
    genearted_text = await ScenarioTalkShowGenerate(
        tg_id=str(tg_id),
        prompt=prompt,
        job=job
    ).generate_message()

    if genearted_text is not None:
        return genearted_text
    else:
        return "Oooops, something wrong. Try request again later..."


@dp.callback_query_handler(text="talk_show_scenario")
async def choose_job_menu_scenario(query: types.CallbackQuery, state: FSMContext):
    await bot.send_chat_action(chat_id=query.message.chat.id, action='typing')
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    except:
        pass

    await state.set_state(TalkShowForm.job)

    await bot.send_message(query.message.chat.id, md.escape_md("This is your moment of glory! 🪄 Tell me which job made you famous?"),
                           reply_markup=await get_choose_job_menu_talk_show_scenario())


@dp.callback_query_handler(state=TalkShowForm.job)
async def process_get_job(query: types.CallbackQuery, state: FSMContext):
    await bot.send_chat_action(chat_id=query.message.chat.id, action='typing')
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    except:
        pass

    job = query.data.split("_")[-1]

    if job != "other":
        await state.set_state(TalkShowForm.start_scenario)

        await state.update_data(job=job)
        await state.update_data(other_job="")


        generate_text = await _genarate_text(
            tg_id=str(query.message.chat.id),
            prompt=await TalkShowPrompt(job=job).get_introduction(),
            job=job
        )

        await bot.send_message(query.message.chat.id, md.escape_md(generate_text))

        question_text = await _genarate_text(
            tg_id=str(query.message.chat.id),
            prompt=await TalkShowPrompt(job=job).get_question(),
            job=job
        )

        await bot.send_message(query.message.chat.id, md.escape_md(question_text))

        await state.update_data(
            previous_questions=question_text,
            job=job
        )

    if job == "other":
        await state.set_state(TalkShowForm.other_job)

        await bot.send_message(query.message.chat.id, md.escape_md("Name a job that made you a celebrity"))


@dp.message_handler(state=TalkShowForm.other_job)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    await state.set_state(TalkShowForm.start_scenario)

    await state.update_data(job=message.text)

    generate_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=message.text).get_introduction(),
        job=message.text
    )

    await bot.send_message(message.chat.id, md.escape_md(generate_text))

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=message.text).get_question(),
        job=message.text
    )

    await bot.send_message(message.chat.id, md.escape_md(question_text))

    await state.update_data(
        previous_questions=question_text,
        job=message.text
    )


@dp.message_handler(state=TalkShowForm.start_scenario)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass
    await state.set_state(TalkShowForm.question_1)

    data = await state.get_data()

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")
    await state.update_data(job=job)

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_1)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    await state.set_state(TalkShowForm.question_2)

    data = await state.get_data()

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_2)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_3)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_3)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_4)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_4)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_5)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_5)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_6)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_6)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_7)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_7)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_8)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_8)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_9)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_9)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_10)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_10)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_11)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_11)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_12)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_12)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_13)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_13)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_14)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_14)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_future)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_future)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.question_advice_to_newcomers)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question_future(previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))


@dp.message_handler(state=TalkShowForm.question_advice_to_newcomers)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    await state.set_state(TalkShowForm.end)

    job = data.get("job")

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_question_advice_to_newcomers(
            previous_questions=data.get('previous_questions')),
        job=job
    )

    await state.update_data(previous_questions=f"{data.get('previous_questions')} {question_text}")

    await bot.send_message(message.chat.id, md.escape_md(question_text))

@dp.message_handler(state=TalkShowForm.end)
async def process_get_other_job(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()

    job = data.get("job")

    await state.clear()

    question_text = await _genarate_text(
        tg_id=str(message.chat.id),
        prompt=await TalkShowPrompt(job=job).get_end(),
        job=job
    )

    await bot.send_message(message.chat.id, md.escape_md(question_text))

    await asyncio.sleep(2)

    await bot.send_message(message.chat.id, md.escape_md("Great! You have completed the scenario 'Talk Show' 💎"),
                           reply_markup=await get_end_menu_talk_show_scenario())
