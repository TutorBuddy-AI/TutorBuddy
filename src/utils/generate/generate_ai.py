import io
import random
import aiohttp
import ast

from typing import Any

from src.config import config


OPENAI_API = ast.literal_eval(config.OPENAI_API)
PROXY = ast.literal_eval(config.PROXY)

class GenerateAI:
    def __init__(self, request_url: str):
        self.headers = {"Authorization": []}
        self.request_url = request_url
        self.COMMUNICATION_TYPE = "json"
        self.TEXT_TO_SPEECH_TYPE = "mpeg"
        self.SPEECH_TO_TEXT_TYPE = "plain"

    async def send_request(self, payload: Any) -> Any:
        self.headers["Authorization"] = random.choice(OPENAI_API)
        proxy = random.choice(PROXY)

        proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.request_url, json=payload, headers=self.headers, proxy=proxy[0],
                                    proxy_auth=proxy_auth) as response:
                if response.status == 200:
                    content_type = response.headers.get("content-type").split("/")[1]

                    if content_type == self.COMMUNICATION_TYPE:
                        return await response.json()

                    elif content_type == self.TEXT_TO_SPEECH_TYPE:
                        return io.BytesIO(await response.read())
                else:
                    return None

    async def send_request_speech_to_text(self, audio_bytes: io.BytesIO, model: str) -> str:
        self.headers["Authorization"] = random.choice(OPENAI_API)
        proxy = random.choice(PROXY)

        proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])

        form_data = aiohttp.FormData()

        form_data.add_field('file', audio_bytes, filename='voice_message.ogg', content_type='audio/ogg')
        form_data.add_field('model', model)
        form_data.add_field("response_format", "text")

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.request_url, data=form_data, headers=self.headers, proxy=proxy[0],
                                    proxy_auth=proxy_auth) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
