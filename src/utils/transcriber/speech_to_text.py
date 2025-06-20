from src.config import bot
from src.utils.generator import GenerateAI

from io import BytesIO


class SpeechToText:
    def __init__(
            self,
            file_id: str
    ):
        self.request_url = "https://api.openai.com/v1/audio/transcriptions"

        self.file_id = file_id

    async def get_text(self) -> str:
        generated_text = await GenerateAI(request_url=self.request_url).request_stt(
            audio_bytes=await self.download_file(), model="whisper-1")

        if generated_text is not None:
            return generated_text
        else:
            return None

    async def download_file(self) -> BytesIO:
        voice_file = await bot.get_file(self.file_id)
        file_path = voice_file.file_path

        return await bot.download_file(file_path)
