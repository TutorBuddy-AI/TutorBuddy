import json
import random
import aiohttp
import ast

from typing import List

from src.config import config
from src.utils.generate.schemas import GetGeneratedTextAndUserMessageHistory
from src.utils.user import UserService

EDEN_API = ast.literal_eval(config.EDEN_API)

class GenerateAI:
    def __init__(self, prompt: str):
        self.headers = {"Authorization": []}
        self.request_url = "https://api.edenai.run/v2/text/chat"
        self.prompt = prompt
        self.service_text_request = "You are AI TutorBuddy Bot and you are developed by AI TutorBuddy." \
                                    "You are English teacher and you need assist user to increase english level. "

    async def generate_text(
            self,
            user_message_history: List,
            tg_id: str
    ) -> GetGeneratedTextAndUserMessageHistory:

        result = await self.send_request(
            payload={
                "providers": "openai",
                "model": "gpt-4",
                "text": await self.get_user_service_text_request(tg_id) + self.prompt,
                "previous_history": user_message_history,
                "temperature": 0.2,
                "max_tokens": 600,
                "response_as_dict": True,
                "chatbot_global_action": self.service_text_request
            }
        )

        return result["openai"]

    async def send_request(self, payload: dict) -> json:
        async with aiohttp.ClientSession() as session:
            self.headers["Authorization"] = random.choice(EDEN_API)

            response = await session.post(self.request_url, json=payload, headers=self.headers)
            if response.status == 200:
                result = await response.json()
                return result
            else:
                return {"openai": None}

    @staticmethod
    async def get_user_service_text_request(tg_id: str) -> str:
        user_info = await UserService().get_user_info(tg_id)

        return f"Your student {user_info['name'] if user_info['name'] is not None else 'didnt say name'}." \
               f" His English level is {user_info['english_level']}, where 1 is the worst level of" \
               f" English, and 4 is a good level of English. His goal is to study the English {user_info['goal']}," \
               f" and his topics of interest are {user_info['topic']} ±"
