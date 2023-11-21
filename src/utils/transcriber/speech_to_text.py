import ast
import random

import aiohttp
import io
import asyncio

from src.config import bot, config

EDEN_API = ast.literal_eval(config.EDEN_API)

class SpeechToText:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "authorization": random.choice(EDEN_API)
        }
        self.request_url = "https://api.edenai.run/v2/audio/speech_to_text_async"

    async def get_text(self, file_id) -> str:
        bytes_io = await self.download_file(file_id)
        public_id = await self.transcribe_speech_to_text(bytes_io)
        url = f"{self.request_url}/{public_id}"

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url=url, headers=self.headers) as response:
                    response_json = await response.json()
                    status = response_json['status']
                    if status == 'processing':
                        await asyncio.sleep(7)
                    elif status == 'finished':
                        return await self.get_speech_to_text(public_id)
                        break

    async def download_file(self, file_id: str) -> io.BytesIO:
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        bytes_io = io.BytesIO(file.read())
        return bytes_io

    async def transcribe_speech_to_text(self, bytes_io: io.BytesIO) -> str:
        async with aiohttp.ClientSession() as session:
            url = self.request_url

            form_data = aiohttp.FormData()
            form_data.add_field('show_original_response', 'False')
            form_data.add_field('speakers', '1')
            form_data.add_field('profanity_filter', 'False')
            form_data.add_field('convert_to_wav', 'True')
            form_data.add_field('providers', 'google')
            form_data.add_field('language', 'en')
            form_data.add_field('custom_vocabulary', '')
            bytes_payload = aiohttp.payload.BytesPayload(bytes_io.getvalue())
            form_data.add_field('file', bytes_payload, filename='audio_file.ogg', content_type='audio/ogg')

            async with session.post(url, data=form_data, headers=self.headers) as response:
                response_json = await response.json()
                public_id = response_json['public_id']

            return public_id

    async def get_speech_to_text(self, public_id: str) -> str:
        url = f"{self.request_url}/{public_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=self.headers) as response:
                data = await response.json()
                return data['results']['google']['text']
