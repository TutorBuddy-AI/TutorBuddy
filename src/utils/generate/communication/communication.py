import json
import logging

from src.utils.const import LANGUAGE_LEVEL_MAPPING
from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory
from src.utils.generate import GenerateAI


class CommunicationGenerate:
    def __init__(
            self,
            tg_id: str,
            prompt: str,
            user_message_history: GetUserMessageHistory
    ):
        self.tg_id = tg_id
        self.prompt = prompt
        self.request_url = "https://api.openai.com/v1/chat/completions"
        self.user_message_history = user_message_history

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
                       f" His English level is '{mapped_level}'. His goal is to study the English"
                       f" {user_info['goal']}, and his topics of interest are {user_info['topic']}."
                       f"You are {user_info['speaker']}. You are developed by AI TutorBuddy."
                       f"You are English teacher and you need assist user to increase english level. "
        }

        extended_history = [service_request]
        extended_history.extend(self.user_message_history)
        extended_history.append({"role": "user", "content": self.prompt})

        prompt_request = (
            f"Please, maintain a friendly conversation - answer to the user's question "
            f"and ask him questions about things that interest him, as if you are his buddy or friend. "
            f"If he starts speaking in a language other than English, give him a gentle reprimand "
            f"and suggest that he start speaking English again. Always answer in English only. "
            f"Write your message using {mapped_level} English level, please"
        )

        extended_history.append({
            "role": "system",
            "content": prompt_request})

        logging.info(f"Extended history [CommunicationGenerate]: {extended_history}")

        return extended_history
