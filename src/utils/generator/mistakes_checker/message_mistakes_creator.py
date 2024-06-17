from src.utils.user.schemas import GetUserMessageHistory
from src.utils.user.user_service import UserService
from src.utils.generator.mistakes_checker import MistakesChecker


class MessageMistakesCreator:
    def __init__(
            self,
            tg_id: str,
            message_text: str
    ):
        self.tg_id = tg_id
        self.message_text = message_text

    async def create_communication_message_text(self) -> str:
        generated_text = await MistakesChecker(
            tg_id=str(self.tg_id),
            user_message_history=await self.get_user_message_history(),
            message_text=self.message_text
        ).generate_mistakes()

        if generated_text is not None:
            return generated_text
        else:
            return "Oooops, something wrong. Try request again later..."

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
