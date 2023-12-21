from src.utils.user.user_service import UserService
from src.utils.generate import GenerateAI
import json

from utils.user.schemas import GetUserMessageHistory


class TranslateGenerate:
    def __init__(
            self,
            tg_id: str,
            user_message_history: GetUserMessageHistory
    ):
        self.tg_id = tg_id
        self.request_url = "https://api.openai.com/v1/chat/completions"
        self.user_message_history = user_message_history

    async def translate(self) -> str:
        payload = await self.get_combine_data()
        generated_text = await GenerateAI(request_url=self.request_url).send_request(payload=payload)

        if generated_text:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def user_native_lang(self) -> str:
        user_info = await UserService().get_user_info(self.tg_id)
        return user_info['native_lang']

    async def get_combine_data(self) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_user_message_history_with_service_text_request_and_prompt(),
            "max_tokens": 400
        }

    async def get_user_message_history_with_service_text_request_and_prompt(self) -> GetUserMessageHistory:
        user_info = await UserService().get_user_info(self.tg_id)
        service_request = {
            "role": "system",
            "content": f"Your student {user_info['name'] if user_info['name'] is not None else 'didnt say name'}."
                       f" His English level is {user_info['english_level']}, where 1 is the worst level of"
                       f" English, and 4 is a good level of English. His goal is to study the English"
                       f" {user_info['goal']}, and his topics of interest are {user_info['topic']}."
                       f"You are {user_info['speaker']}. You are developed by AI TutorBuddy."
                       f"You are English teacher and you need assist user to increase english level. "
        }

        translate_request = {
            "role": "system",
            "content":
                f"User didn't understand your last message, "
                f"Please translate it into {await self.user_native_lang()}. "
        }
        self.user_message_history[0] = service_request
        self.user_message_history.append(translate_request)
        return self.user_message_history
