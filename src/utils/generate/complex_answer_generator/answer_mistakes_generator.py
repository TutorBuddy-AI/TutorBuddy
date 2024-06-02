import json
import logging
from typing import Optional, Dict

from src.utils.const import LANGUAGE_LEVEL_MAPPING
from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory
from src.utils.generate import GenerateAI

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from src.utils.generate.complex_answer_generator.answer_schema import answer_schema


class AnswerMistakesGenerator:
    """
    Class to generate AI's answer on user's message in JSON format
    with the list of user's mistakes
    """

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

    async def generate_message(self) -> Optional[Dict[str, object]]:
        generated_text = await GenerateAI(request_url=self.request_url).request_gpt(
            payload=await self.get_combine_data())

        if generated_text is not None:
            return await self.parse_answer(generated_text["choices"][0]["message"]["content"])
        else:
            return None

    @staticmethod
    async def validate_answer(answer_json: str) -> bool:
        try:
            validate(instance=answer_json, schema=answer_schema)
        except ValidationError as err:
            return False
        return True

    async def parse_answer(self, answer_json: str) -> Optional[Dict[str, object]]:
        try:
            loaded_json = json.loads(answer_json)
        except ValueError as err:
            return None
        if await self.validate_answer(loaded_json):
            return loaded_json
        return None

    async def get_combine_data(self) -> json:
        return {
            "model": "gpt-3.5-turbo",
            "messages": await self.get_user_message_history_with_service_text_request_and_prompt(),
            "max_tokens": 400
        }

    async def get_user_message_history_with_service_text_request_and_prompt(self) -> GetUserMessageHistory:
        user_info = await UserService().get_user_person(self.tg_id)
        mapped_level = LANGUAGE_LEVEL_MAPPING[user_info['english_level']]
        answer_request = {
            "role": "system",
            "content": """
                    Please, give an answer on the last user's message in JSON format with the following schema: 
                    { 
                    "answer": "{text_of_the_answer}", 
                    "mistakes": ["{mistake1}", "{mistake2}"] 
                    } 
                    "mistakes" parameter should be replaced with the list of strings with the explanation of grammatical 
                    and punctuation user's mistakes, that he made in his last message with suggested options to correct 
                    those mistakes, if the last user's message is grammatically correct, doesn't have any punctuation 
                    mistakes and all of words were used properly, the list may be empty. 
                    text_of_the_answer should be replaced with the text of the answer for user,
                    Please, keep the conversation friendly and engaging. 
                    Answer the user's questions and inquire about topics that interest him, 
                    as if you're chatting with a friend to keep the conversation going.Always conclude your responses with a relevant question to ensure the conversation continues on an engaging note. 
                    Don't allow the dialog to finish on you.
                    Entertain your interlocutor. 
                    If the conversation shifts to a language other than English, kindly remind them to continue in English. 
                    Always respond in English only.
                    """ + f" Write your message using {mapped_level} English level, please"
                          "There should be nothing else in the text except this json"
        }
        service_request = {
            "role": "system",
            "content": f"You are an English teacher."
                       f"I am your student {user_info['name'] if user_info['name'] is not None else 'didnt say name'} with English level {mapped_level}, let's chat for practice."
                       f"I am interested in topics about {user_info['topic']} and my goals is {user_info['goal']}."
                       f"Use colloquialisms in the dialogue."
                       f"Don't send everything at once! Ask a question, wait for me to answer."
                       f"If I answer briefly, don't repeat the question, but ask a detailed and new question, or ask a clarification or a new question."
                       f"Always end with a question!"
                       f"Add appropriate emoticons, as if we are communicating in a friendly way. "
                       f"Write answers of no more than 100 characters\n"
            + answer_request["content"]
        }
        extended_history = [service_request]
        extended_history.extend(self.user_message_history)
        extended_history.append({"role": "user", "content": self.prompt})

        logging.info(f"Extended history [AnswerMistakesGenerator]: {extended_history}")

        return extended_history
