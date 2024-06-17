import json
import logging
from typing import Optional

from src.utils.const import LANGUAGE_LEVEL_MAPPING
from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory
from src.utils.generator import GenerateAI


class NewsGreetingsGenerator:
    def __init__(
            self
    ):
        self.request_url = "https://api.openai.com/v1/chat/completions"

    async def generate_message(self) -> Optional[str]:
        generated_text = await GenerateAI(request_url=self.request_url).request_gpt(
            payload=await self.get_combine_data())

        if generated_text is not None:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def get_combine_data(self) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_payload(),
            "max_tokens": 100
        }

    async def get_payload(self) -> GetUserMessageHistory:

        service_request = {
            "role": "system",
            "content":
                (
                    "Write a greeting saying that there is a new batch of fresh, interesting news' summaries "
                    "and you suggest reading it and discussing it together.\n"
                    "Insert appropriate emojis in the text."
                    "The greeting should be short (1-2 short sentences). "
                    "and it should be understandable for someone who knows English at A1 level"
                )
        }

        payload = [service_request]

        return payload
