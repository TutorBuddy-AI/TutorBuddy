from src.utils.transcriber import TextToSpeechOpenAI, TextToSpeechEleven
from src.utils.user import UserService


class TextToSpeech:
    def __init__(self, prompt: str, tg_id: str):
        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self):
        id_voice = await self.get_id_voice()
        if id_voice == "TutorBuddy":
            audio = await TextToSpeechOpenAI(prompt=self.prompt, tg_id=str(self.tg_id)).get_speech()
        else:
            audio = await TextToSpeechEleven(prompt=self.prompt, tg_id=str(self.tg_id)).get_speech(id_voice)
        return audio

    async def get_id_voice(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)
        return user_info["speaker"]

    @staticmethod
    async def get_speech_by_voice(voice, text):
        if voice == "TutorBuddy":
            audio = await TextToSpeechOpenAI.get_speech_for_text(text)
        else:
            audio = await TextToSpeechEleven.get_speech_for_text(text, voice)
        return audio
