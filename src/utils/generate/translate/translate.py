from src.utils.user.user_service import UserService
from src.utils.generate import GenerateAI
import json


class TranslateGenerate:
    """На вход подаётся английский текст, на выходе переведённый текст на родной язык юзера"""
    def __init__(
            self,
            tg_id: str,
            en_string: str
    ):
        self.eng_string = en_string
        self.tg_id = tg_id
        self.request_url = "https://api.openai.com/v1/chat/completions"

    async def translate(self) -> str:
        payload = await self.get_combined_data()
        generated_text = await GenerateAI(request_url=self.request_url).send_request(payload)

        if generated_text:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

    async def get_combine_data(self) -> json:
        user_info = await UserService().get_user_info(self.tg_id)
        return {
            "model": "gpt-3.5-turbo",
            "messages": f"Translate it '{self.eng_string}' on {user_info['native_lang']}",
            "max_tokens": 400
        }