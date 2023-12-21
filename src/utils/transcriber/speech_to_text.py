from src.config import bot, config
from src.utils.generate import GenerateAI

import ast

from io import BytesIO


OPENAI_API = ast.literal_eval(config.OPENAI_API)


class SpeechToText:
    def __init__(
            self,
            file_id: str
    ):
        self.request_url = "https://api.openai.com/v1/audio/transcriptions"

        self.file_id = file_id

    async def get_text(self) -> str:
        generated_text = await GenerateAI(request_url=self.request_url).send_request_speech_to_text(
            audio_bytes=await self.download_file(), model="whisper-1")

        if generated_text is not None:
            return generated_text
        else:
            return None

    async def download_file(self) -> BytesIO:
        voice = await bot.get_file(self.file_id)

        return await bot.download_file_by_id(voice.file_id)





