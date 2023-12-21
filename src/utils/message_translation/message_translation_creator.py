from utils.generate.translate.translate import TranslateGenerate
from utils.user import UserService
from utils.user.schemas import GetUserMessageHistory


class MessageTranslationCreator:
    def __init__(
            self,
            tg_id: str
    ):
        self.tg_id = tg_id

    async def create_communication_message_text(self) -> str:
        generated_text = await TranslateGenerate(
            tg_id=str(self.tg_id),
            user_message_history=await self.get_user_message_history()
        ).translate()

        if generated_text is not None:
            return generated_text
        else:
            return "Oooops, something wrong. Try request again later..."

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
