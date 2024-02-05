from utils.transcriber import TextToSpeechOpenAI, TextToSpeechEleven
from utils.user import UserService


class TextToSpeech:
    def __init__(self, prompt: str, tg_id: str):
        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self):
        voice = await self.get_id_voice()
        if voice == 'Anastasia':
            audio = await TextToSpeechEleven(prompt=self.prompt, tg_id=str(self.tg_id)).get_speech()
        else:
            audio = await TextToSpeechOpenAI(prompt=self.prompt, tg_id=str(self.tg_id)).get_speech()
        return audio

    async def get_id_voice(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)

        return user_info["speaker"] == "Anastasia"