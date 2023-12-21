from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    native_language = State()
    goal = State()
    english_level = State()
    topic = State()


class NewValueUserInfo(StatesGroup):
    new_value = State()

class FormSupport(StatesGroup):
    message = State()

class FormFeedback(StatesGroup):
    message = State()

class FormName(StatesGroup):
    new_name = State()

class FormTopic(StatesGroup):
    new_topic = State()

class FormSpeaker(StatesGroup):
    new_speaker = State()

class FormNativeLanguage(StatesGroup):
    new_native_language = State()

class FormEnglishLevel(StatesGroup):
    new_english_level = State()