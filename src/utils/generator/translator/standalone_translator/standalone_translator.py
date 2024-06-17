import logging

from src.utils.user.user_service import UserService
from src.utils.generator import GenerateAI
import json

from src.utils.user.schemas import GetUserMessageHistory


class StandaloneTranslator:
    def __init__(
            self,
            tg_id: str,
            message_text: str,
            lang: str
    ):
        self.tg_id = tg_id
        self.request_url = "https://api.openai.com/v1/chat/completions"
        self.message_text = message_text
        self.lang = lang

    async def translate(self, max_tokens: int = 100) -> str:
        payload = await self.get_combine_data(max_tokens)
        generated_text = await GenerateAI(request_url=self.request_url).request_gpt(payload=payload)
        if generated_text:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def user_native_lang(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)
        return user_info['native_lang']

    async def get_combine_data(self, max_tokens: int = 100) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_user_message_history_with_service_text_request_and_prompt(),
            "max_tokens": max_tokens
        }

    async def get_user_message_history_with_service_text_request_and_prompt(self) -> GetUserMessageHistory:

        translate_request = {
            "role": "system",
            "content":
                f'Please translate this message: "{self.message_text}" into {self.lang}.'
        }

        extended_history = [translate_request]

        logging.info(f"Extended history [TranslateGenerate]: {extended_history}")

        return extended_history
