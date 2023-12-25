from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.commands.scenario.TalkShow.state_talk_show import StateTalkShow
from aiogram import types, md
from src.commands.scenario.keyboard import menu_scenario_keyboard, menu_talk_show_keyboard


@dp.callback_query_handler(text="talk_show_scenario")
async def menu_scenario(query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)

        await bot.send_message(chat_id=query.message.chat.id,
                               text="This is your moment of glory! 🪄 Tell me which job made you famous?",
                               reply_markup=menu_scenario_keyboard)

    except:
        pass


@dp.callback_query_handler(text="talk_show_scenario")
async def start_talk_show_scenario(query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)

        await bot.send_message(chat_id=query.message.chat.id,
                               text="Tell me how you chose the job of a racer. What inspired you to become a race car driver? 🏎️")

        await StateTalkShow.waiting_for_job.set()
    except:
        pass


# тут выбор кнопок из job,other,get back


# Select job
@dp.message_handler(state=StateTalkShow.waiting_for_job)
async def process_job_message(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() == 'job':
            await bot.send_message(chat_id=message.chat.id, text="Hellosdasd")

            await StateTalkShow.question_1.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_1)
async def process_question_1(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Your latest album has received widespread acclaim and has been praised for its emotional depth and powerful storytelling. Can you share some insights into the inspiration behind the music and the creative process that went into crafting this album?")

        await state.update_data(question_1_answer=message.text)
        await StateTalkShow.question_2.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_2)
async def process_question_2(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Your live performances are known for their electrifying energy and emotional intensity. How do you prepare for a live show, and what do you hope to convey to your audience through your performances?")

        await state.update_data(question_2_answer=message.text)
        await StateTalkShow.question_3.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_3)
async def process_question_3(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="As a prominent figure in the music industry, how do you navigate the pressures and expectations that come with fame while staying true to yourself as an artist?")

        await state.update_data(question_3_answer=message.text)
        await StateTalkShow.question_4.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_4)
async def process_question_4(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Off the field, you've been actively involved in philanthropy and community initiatives. How do you use your platform as a football star to make a positive impact on society, and what causes are particularly close to your heart?")

        await state.update_data(question_4_answer=message.text)
        await StateTalkShow.question_5.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_5)
async def process_question_5(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="The concept of mentorship and guidance is crucial in fostering talent and growth. Can you share the impact that mentors or influential figures have had on your journey, and how do you pay it forward to nurture the next generation of artists?")

        await state.update_data(question_5_answer=message.text)
        await StateTalkShow.question_6.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_6)
async def process_question_6(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="What do you hope audiences take away from watching this film?")

        await state.update_data(question_6_answer=message.text)
        await StateTalkShow.question_7.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_7)
async def process_question_7(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="What was the most rewarding part of working on this project?")

        await state.update_data(question_7_answer=message.text)
        await StateTalkShow.question_8.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_8)
async def process_question_8(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Your latest [project/album/film/match] has garnered widespread acclaim. Can you take us through the creative process and the personal significance behind this work?")

        await state.update_data(question_8_answer=message.text)
        await StateTalkShow.question_9.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_9)
async def process_question_9(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Collaboration is integral to creativity and innovation. Can you share some insights into your approach to working with fellow artists and collaborators to bring your vision to life?")

        await state.update_data(question_9_answer=message.text)
        await StateTalkShow.question_10.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_10)
async def process_question_10(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Can you take us back to the beginning of your journey as a racer and share what initially sparked your passion for the sport of Formula 1?")
        await state.update_data(question_10_answer=message.text)
        await StateTalkShow.question_11.set()

    except Exception as e:
        pass


@dp.message_handler(state=StateTalkShow.question_10)
async def process_question_10(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Away from the race track, what are some of the passions and pursuits that offer you solace and fulfillment, and how do you strike a balance between your professional and personal life?")

        await state.update_data(question_10_answer=message.text)
        await StateTalkShow.question_11.set()

    except Exception as e:
        pass
