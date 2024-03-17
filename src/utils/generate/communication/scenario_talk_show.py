import json
import logging

from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory
from src.utils.generate import GenerateAI


class ScenarioTalkShowGenerate:
    def __init__(
            self,
            tg_id: str,
            prompt: str,
            job: str
    ):
        self.tg_id = tg_id
        self.prompt = prompt
        self.job = job
        self.request_url = "https://api.openai.com/v1/chat/completions"

    async def generate_message(self) -> str:
        generated_text = await GenerateAI(request_url=self.request_url).request_gpt(
            payload=await self.get_combine_data())

        if generated_text is not None:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def get_combine_data(self) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_service_text_request_and_prompt(),
            "max_tokens": 50
        }

    async def get_service_text_request_and_prompt(self) -> GetUserMessageHistory:
        user_info = await UserService().get_user_info(self.tg_id)

        service_request = {
            "role": "system",
            "content": f"You're the host of a talk show. Your guest's name is {user_info['name']}. Address him by his"
                       f" first name only. He is very famous in {self.job}. His native language is"
                       f" {user_info['native_lang']}, but you must communicate with him only in English."
                       f" Communicate with him in conversational English"
        }

        extended_history = [service_request]
        extended_history.append({"role": "user", "content": self.prompt})

        logging.info(f"Extended history [ScenarioTalkShowGenerate]: {extended_history}")

        return extended_history
