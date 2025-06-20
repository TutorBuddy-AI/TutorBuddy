from src.utils.user.schemas import GetUserMessageHistory
from src.utils.user.user_service import UserService
from src.utils.generator.hint_generator.hint_generator import HintGenerator


class MessageHintCreator:
    def __init__(
            self,
            tg_id: str
    ):
        self.tg_id = tg_id

    async def create_communication_message_text(self) -> str:
        generated_text = await HintGenerator(
            tg_id=str(self.tg_id),
            user_message_history=await self.get_user_message_history()
        ).generate_hint()

        if generated_text is not None:
            return generated_text

        else:
            return "Oooops, something wrong. Try request again later..."

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
