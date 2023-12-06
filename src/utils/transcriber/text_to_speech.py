from src.utils.user import UserService
from src.utils.generate import GenerateAI
from src.config import config

import ast
import json

from io import BytesIO


OPENAI_API = ast.literal_eval(config.OPENAI_API)


class TextToSpeech:
    def __init__(
            self,
            prompt: str,
            tg_id: str
    ):
        self.request_url = "https://api.openai.com/v1/audio/speech"
        self.man_providers = "echo"
        self.girl_providers = "nova"

        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self) -> BytesIO:
        generated_audio = await GenerateAI(request_url=self.request_url).send_request(
            payload=await self.get_combine_data())

        if generated_audio is not None:
            return generated_audio
        else:
            return None

    async def get_combine_data(self) -> json:
        user_info = await self.get_user_speaker_and_english_level()

        provider = self.girl_providers if user_info[0] == "Anastasia" else self.man_providers
        speed = 0.8 if 1 <= int(user_info[1]) <= 2 else 1.0

        return {
            "model": "tts-1-hd",
            "voice": provider,
            "input": self.prompt,
            "speed": speed
        }

    async def get_user_speaker_and_english_level(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)

        return user_info["speaker"], user_info["english_level"]
