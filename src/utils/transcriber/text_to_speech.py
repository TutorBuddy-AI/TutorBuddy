import ast
import random

import aiohttp
import asyncio
import io

from src.config import config


EDEN_API = ast.literal_eval(config.EDEN_API)


class TextToSpeech:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "authorization": random.choice(EDEN_API)
        }
        self.request_url = "https://api.edenai.run/v2/audio/text_to_speech_async"
        self.providers = "lovoai"

    async def get_speech(self, text: str):
        public_id = await self.post_text_to_speech(text)
        await self.get_text_to_speech(public_id)
        url = f"{self.request_url}/{public_id}"

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url, headers=self.headers) as response:
                    data = await response.json()
                    if 'status' in data:
                        status = data['status']
                        if status == 'processing':
                            await asyncio.sleep(15)
                        elif status == 'finished':
                            audio_resource_url = data['results'][f'{self.providers}']['audio_resource_url']
                            bytes_io = await self.download_audio(audio_resource_url)
                            return bytes_io
                    else:
                        print("Статус не найден в ответе.")
                        break

    async def post_text_to_speech(self, text: str) -> int:
        url = self.request_url

        payload = {
            "show_original_response": False,
            "fallback_providers": "",
            "providers": self.providers,
            "language": "en-US",
            "option": "MALE",
            "text": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                result = await response.json()
                public_id = result['public_id']
                return public_id

    async def get_text_to_speech(self, public_id):
        url = f"{self.request_url}/{public_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                await response.text()

    async def download_audio(self, audio_url):
        url = audio_url

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    bytes_io = io.BytesIO(data)
                    return bytes_io