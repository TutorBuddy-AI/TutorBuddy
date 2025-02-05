from io import BytesIO
from typing import Union, Iterator, Optional

import aiohttp
import ast
import random

from src.utils.user import UserService
from src.config import config

import json

#voice_map = {
#    "Anastasia": "LC58oHYbe1EOt8kPZizM",
#    "AA_Lingua": "sKSCI18qgaDgCq3gTkK2",
#    "Oksana": "YFczjBOHj0ctMzjDRucv",
#    "Victoria": "8I0H65fHjSCx1F4euIr2",
#    "Katya": "5RllsHnSnaXfc2WZkmVt"
#}

#voice_map = {
#    "Anastasia": "FzW9M9JllhhnDKM1GfXg",
#    "AA_Lingua": "aWos4XjccYOxWnzmCLof",
#    "Oksana": "YFczjBOHj0ctMzjDRucv",
#    "Victoria": "8I0H65fHjSCx1F4euIr2",
#    "Katya": "5RllsHnSnaXfc2WZkmVt"
#}

voice_map = {
    "Anastasia": config.VOICE_ID_ANASTASIA,
    "AA_Lingua": config.VOICE_ID_AA_LINGUA,
    "Oksana": config.VOICE_ID_OKSANA,
    "Victoria": config.VOICE_ID_VICTORIA,
    "Katya": config.VOICE_ID_KATYA
}

model = "eleven_multilingual_v2"
request_url = "https://api.elevenlabs.io/v1/text-to-speech/"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": config.ELEVENLABS_API
}

PROXY = ast.literal_eval(config.PROXY)


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
            proxy = random.choice(PROXY)
            proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])
            async with session.post(
                    url=f"{request_url}{voice_map[voice]}",
                    json=await TextToSpeechEleven.get_combine_data(self.prompt),
                    headers=headers,
                    proxy=proxy[0], proxy_auth=proxy_auth) as response:
                if response.status == 200:
                    print(f"Response: {response}")
                    return BytesIO(await response.read())
                else:
                    print(f"Response: {response}")
                    return None

    @staticmethod
    async def get_speech_for_text(text, voice: str) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            proxy = random.choice(PROXY)
            proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])
            async with session.post(
                    url=f"{request_url}{voice_map[voice]}",
                    json=await TextToSpeechEleven.get_combine_data(text),
                    headers=headers,
                    proxy=proxy[0], proxy_auth=proxy_auth) as response:
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
