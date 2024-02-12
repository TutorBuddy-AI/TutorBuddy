from typing import Any

from src.utils.user import UserService
from src.utils.generate import GenerateAI
from src.config import config

import ast
import json

from io import BytesIO

OPENAI_API = ast.literal_eval(config.OPENAI_API)

request_url = "https://api.openai.com/v1/audio/speech"
man_providers = "echo"


class TextToSpeechOpenAI:
    def __init__(
            self,
            prompt: str,
            tg_id: str
    ):
        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self) -> BytesIO:
        generated_audio = await GenerateAI(request_url=request_url).send_request(
            payload=await self.get_combine_data())

        if generated_audio is not None:
            return generated_audio
        else:
            return None
    @staticmethod
    async def get_speech_for_text(text) -> BytesIO:
        generated_audio = await GenerateAI(request_url=request_url).send_request(
            payload=await TextToSpeechOpenAI.get_combine_data_simple(text))

        if generated_audio is not None:
            return generated_audio
        else:
            return None

    async def get_combine_data(self) -> json:
        english_level = await self.get_english_level()
        speed = 0.8 if 1 <= int(english_level) <= 2 else 1.0

        return {
            "model": "tts-1-hd",
            "voice": man_providers,
            "input": self.prompt,
            "speed": speed
        }
    @staticmethod
    async def get_combine_data_simple(text) -> json:

        return {
            "model": "tts-1-hd",
            "voice": man_providers,
            "input": text,
            "speed": 1.0
        }

    async def get_english_level(self) -> int:
        user_info = await UserService().get_user_info(self.tg_id)

        return int(user_info["english_level"])
