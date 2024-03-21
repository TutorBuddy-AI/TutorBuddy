from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    other_name = State()
    native_language = State()
    other_language = State()
    goal = State()
    other_goal = State()
    english_level = State()
    topic = State()
    additional_topic = State()


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
    new_additional_topic = State()


class FormSpeaker(StatesGroup):
    new_speaker = State()


class FormNativeLanguage(StatesGroup):
    new_native_language = State()
    new_other_native_language = State()


class FormEnglishLevel(StatesGroup):
    new_english_level = State()


class FormInitTalk(StatesGroup):
    init_user_message = State()
