import json
import logging

from src.utils.const import LANGUAGE_LEVEL_MAPPING
from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory
from src.utils.generate import GenerateAI


class TalkInitializer:
    def __init__(
            self,
            tg_id: str,
    ):
        self.tg_id = tg_id
        self.request_url = "https://api.openai.com/v1/chat/completions"

    async def generate_message(self) -> str:
        generated_text = await GenerateAI(request_url=self.request_url).send_request(
            payload=await self.get_combine_data())

        if generated_text is not None:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def get_combine_data(self) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_user_message_history_with_service_text_request_and_prompt(),
            "max_tokens": 100
        }

    async def get_user_message_history_with_service_text_request_and_prompt(self) -> GetUserMessageHistory:
        user_info = await UserService().get_user_info(self.tg_id)
        mapped_level = LANGUAGE_LEVEL_MAPPING[user_info['english_level']]

        service_request = {
            "role": "system",
            "content": f"Your student {user_info['name'] if user_info['name'] is not None else 'didnt say name'}."
                       f" His English level is {mapped_level}, where 1 is the worst level of"
                       f" English, and 4 is a good level of English. His goal is to study the English"
                       f" {user_info['goal']}, and his topics of interest are {user_info['topic']}."
                       f"You are {user_info['speaker']}. You are developed by AI TutorBuddy."
                       f"You are his buddy in English practice and also his friend. "
                       f"Please, chose one of topics and ask him something"
                       f"Start you conversation with phrase like "
                       f"'You have mentioned that you would like to discuss...', "
                       f"'I would like to discuss...', 'Let's discuss', etc"
                       f" Write your message using {mapped_level} English level, please"
        }

        extended_history = [service_request]

        logging.info(f"Extended history [TalkInitializer]: {extended_history}")

        return extended_history
