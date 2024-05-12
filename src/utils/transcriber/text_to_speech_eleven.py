from io import BytesIO
from typing import Union, Iterator, Optional

import aiohttp

from src.utils.user import UserService
from src.config import config

import json

voice_map = {
    "Anastasia": "LC58oHYbe1EOt8kPZizM",
    "AA_Lingua": "sKSCI18qgaDgCq3gTkK2",
    "Oksana": "YFczjBOHj0ctMzjDRucv",
    "Victoria": "8I0H65fHjSCx1F4euIr2",
    "Ekaterina": "5RllsHnSnaXfc2WZkmVt"
}


model = "eleven_multilingual_v2"
request_url = "https://api.elevenlabs.io/v1/text-to-speech/"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": config.ELEVENLABS_API
}


class TextToSpeechEleven:
    def __init__(
            self,
            prompt: str,
            tg_id: str
    ):
        self.prompt = prompt
        self.tg_id = tg_id

    async def get_speech(self, voice: str) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{request_url}{voice_map[voice]}",
                    json=await TextToSpeechEleven.get_combine_data(self.prompt),
                    headers=headers) as response:
                if response.status == 200:
                    print(f"Response: {response}")
                    return BytesIO(await response.read())
                else:
                    return None

    @staticmethod
    async def get_speech_for_text(text, voice: str) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{request_url}{voice_map[voice]}",
                    json=await TextToSpeechEleven.get_combine_data(text),
                    headers=headers) as response:
                if response.status == 200:
                    print(f"Response: {response}")
                    return BytesIO(await response.read())
                else:
                    print(f"Response: {response}")
                    return None

    @staticmethod
    async def get_combine_data(text) -> json:
        return {
            "text": text,
            "model_id": model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.1,
                "use_speaker_boost": True,
            },
        }
