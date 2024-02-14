from src.utils.generate.standalone_translator.standalone_translator import StandaloneTranslator
from src.utils.generate.translate.translate import TranslateGenerate
from src.utils.user import UserService
from src.utils.user.schemas import GetUserMessageHistory


class MessageTranslationCreator:
    def __init__(
            self,
            tg_id: str
    ):
        self.tg_id = tg_id

    async def create_communication_message_text(self, message_text: str) -> str:
        generated_text = await TranslateGenerate(
            tg_id=str(self.tg_id),
            message_text=message_text,
            user_message_history=await self.get_user_message_history()
        ).translate()

        if generated_text is not None:
            return generated_text
        else:
            return "Oooops, something wrong. Try request again later..."

    async def create_communication_message_text_standalone(self, message_text: str, lang: str) -> str:
        generated_text = await StandaloneTranslator(
            tg_id=str(self.tg_id),
            message_text=message_text,
            lang=lang
        ).translate()

        if generated_text is not None:
            return generated_text
        else:
            return "Oooops, something wrong. Try request again later..."

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
