from io import BytesIO
from typing import Union, Iterator, Optional

import aiohttp

from src.utils.user import UserService
from src.config import config

import json

id_bot_voice = "SQbRRoMNiJau4LetNtC3"
id_nastya_voice = "LC58oHYbe1EOt8kPZizM"
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

    async def get_speech(self) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{request_url}{id_nastya_voice}",
                    json=await TextToSpeechEleven.get_combine_data(self.prompt),
                    headers=headers) as response:
                if response.status == 200:
                    print(f"Response: {response}")
                    return BytesIO(await response.read())
                else:
                    return None

    @staticmethod
    async def get_speech_for_text(text) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{request_url}{id_nastya_voice}",
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
