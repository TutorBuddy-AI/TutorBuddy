from src.utils.user.user_service import UserService
from src.utils.generate import GenerateAI
import json


class Translate:
    """На вход подаётся английский текст, на выходе переведённый текст на родной язык юзера"""
    def __init__(
            self,
            tg_id: str,
            en_string: str
    ):
        self.eng_string = en_string
        self.tg_id = tg_id
        self.request_url = "https://api.openai.com/v1/chat/completions"

    async def translate_string(self) -> str:
        user_info = await user.get_user_info(tg_id=self.tg_id)

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": f"Translate it '{self.eng_string}' on {user_info['native_lang']}",
            "max_tokens": 400,
        }

        generated_text = await GenerateAI(request_url=self.request_url).send_request(
            payload=payload)

        print(generated_text)

        if generated_text:
            return generated_text["choices"][0]["message"]["content"]
        else:
            return None

