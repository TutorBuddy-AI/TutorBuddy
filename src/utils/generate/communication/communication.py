import json

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

        extended_history = [service_request]
        extended_history.extend(self.user_message_history)
        extended_history.append({"role": "user", "content": self.prompt})

        return extended_history
