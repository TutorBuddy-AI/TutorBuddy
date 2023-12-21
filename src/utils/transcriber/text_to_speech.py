from typing import Union, Iterator

import aiohttp

from src.utils.user import UserService
from src.config import config

import ast
import json


OPENAI_API = ast.literal_eval(config.OPENAI_API)


class TextToSpeech:
    def __init__(
            self,
            prompt: str,
            tg_id: str
    ):
        self.id_bot_voice = "8jLmaTrLPyjjGe8C89W7"
        self.id_nastya_voice = "cCglcvSMLdXuPYb9kXDB"
        self.model = "eleven_multilingual_v2"
        self.request_url = "https://api.elevenlabs.io/v1/text-to-speech/"

        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": config.ELEVENLABS_API
        }

        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self) -> Union[bytes, Iterator[bytes]]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{self.request_url}{await self.get_id_voice()}",
                    json=await self.get_combine_data(),
                    headers=self.headers) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    return None

    async def get_combine_data(self) -> json:
        return {
            "text": self.prompt,
            "model_id": self.model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.1,
                "use_speaker_boost": True,
            },
        }

    async def get_id_voice(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)

        return self.id_nastya_voice if user_info["speaker"] == "Anastasia" else self.id_bot_voice
