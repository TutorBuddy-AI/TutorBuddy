from src.database.models import MessageHistory
from src.database import Transactional, session
from src.utils.user.schemas import GetUserMessageHistory, GetNewUserMessageHistory
from src.utils.user import UserService
from src.utils.generate.communication import CommunicationGenerate


class UserCreateMessage:
    def __init__(
            self,
            tg_id: str,
            prompt: str,
            type_message: str
    ):
        self.tg_id = tg_id
        self.prompt = prompt
        self.type_message = type_message

    async def create_communication_message_text(self) -> str:
        generated_text = await CommunicationGenerate(
            tg_id=str(self.tg_id),
            prompt=self.prompt,
            user_message_history=await self.get_user_message_history()
        ).generate_message()

        if generated_text is not None:
            await self.save_to_database_message_history(
                new_user_message_history=[
                    {"role": "user", "content": self.prompt},
                    {"role": "assistant", "content": generated_text}
                ]
            )

            return generated_text

        else:
            return "Oooops, something wrong. Try request again later..."

    @Transactional()
    async def save_to_database_message_history(
            self,
            new_user_message_history: GetNewUserMessageHistory
    ) -> None:
        for row in new_user_message_history:
            message_history = MessageHistory(
                tg_id=str(self.tg_id),
                message=row["content"],
                role=row["role"],
                type=self.type_message
            )

            session.add(message_history)

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
