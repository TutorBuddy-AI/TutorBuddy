import asyncio
import io
import logging
import random
from asyncio import Event

import aiohttp
import ast

from typing import Any, Optional

from src.config import config
from src.config.initialize import open_ai_token_limiters
from src.utils.api_limiter.APILimiter import APILimiter

PROXY = ast.literal_eval(config.PROXY)

GPT3_DELAY = 60.0 / 500
TTS_DELAY = 60.0 / 50
STT_DELAY = 60.0 / 50


class GenerateAI:
    def __init__(self, request_url: str):
        self.headers = {"Authorization": []}
        self.request_url = request_url
        self.COMMUNICATION_TYPE = "json"
        self.TEXT_TO_SPEECH_TYPE = "mpeg"
        self.SPEECH_TO_TEXT_TYPE = "plain"

    async def wait(self, waiting_event: Event, time_to_wait: float):
        """Waiting coroutine is needed to reset event and allow new request"""
        await asyncio.sleep(time_to_wait)
        waiting_event.set()

    async def request_gpt(self, payload: Any) -> Any:
        async with aiohttp.ClientSession() as session:
            token_limiter: APILimiter = random.choice(open_ai_token_limiters)

            self.headers["Authorization"] = token_limiter.token
            event = token_limiter.gpt3_waiting_event
            lock = token_limiter.gpt3_lock

            proxy = random.choice(PROXY)

            proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])
            async with lock:
                await event.wait()
                event.clear()  # event is needed to implement timeout between requests
                response = await session.post(url=self.request_url, json=payload,
                                              headers=self.headers, proxy=proxy[0], proxy_auth=proxy_auth)
                waiting_task = asyncio.create_task(self.wait(event, GPT3_DELAY))
                await asyncio.sleep(0)  # it's needed to execute waiting task

            if response.status == 200:
                logging.info(f"Good response [GenerateAI]: {response}")
                content_type = response.headers.get("content-type").split("/")[1]

                if content_type == self.COMMUNICATION_TYPE:
                    return await response.json()

                elif content_type == self.TEXT_TO_SPEECH_TYPE:
                    return io.BytesIO(await response.read())
            else:
                logging.info(f"Bad response [GenerateAI]: {response}")
                return None

    async def request_stt(self, audio_bytes: io.BytesIO, model: str) -> Any:
        form_data = aiohttp.FormData()

        form_data.add_field('file', audio_bytes, filename='voice_message.ogg', content_type='audio/ogg')
        form_data.add_field('model', model)
        form_data.add_field("response_format", "text")

        async with aiohttp.ClientSession() as session:
            token_limiter: APILimiter = random.choice(open_ai_token_limiters)

            self.headers["Authorization"] = token_limiter.token
            event = token_limiter.stt_waiting_event
            lock = token_limiter.stt_lock

            proxy = random.choice(PROXY)

            proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])
            async with lock:
                await event.wait()
                event.clear()
                response = await session.post(url=self.request_url, data=form_data,
                                              headers=self.headers, proxy=proxy[0], proxy_auth=proxy_auth)
                waiting_task = asyncio.create_task(self.wait(event, STT_DELAY))  # creation of background task
                await asyncio.sleep(0)  # it's needed to execute waiting task

            if response.status == 200:
                return await response.text()
            else:
                return None

    async def request_tts(self, payload: Any) -> Any:
        async with aiohttp.ClientSession() as session:
            token_limiter: APILimiter = random.choice(open_ai_token_limiters)

            self.headers["Authorization"] = token_limiter.token
            lock = token_limiter.tts_lock
            event = token_limiter.tts_waiting_event

            proxy = random.choice(PROXY)

            proxy_auth = aiohttp.BasicAuth(proxy[1], proxy[2])
            async with lock:
                await event.wait()
                event.clear()
                response = await session.post(url=self.request_url, json=payload,
                                              headers=self.headers, proxy=proxy[0], proxy_auth=proxy_auth)
                waiting_task = asyncio.create_task(self.wait(event, TTS_DELAY))  # creation of background task
                await asyncio.sleep(0)  # it's needed to execute waiting task

            if response.status == 200:
                content_type = response.headers.get("content-type").split("/")[1]

                if content_type == self.COMMUNICATION_TYPE:
                    return await response.json()

                elif content_type == self.TEXT_TO_SPEECH_TYPE:
                    return io.BytesIO(await response.read())
            else:
                logging.info(f"Bad response [GenerateAI]: {response}")
                return None
