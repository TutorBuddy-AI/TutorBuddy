from datetime import timedelta, datetime
from typing import List

from src.database.models import MessageHistory
from src.database import Transactional, session
from src.utils.user.schemas import GetUserMessageHistory, GetNewUserMessageHistory
from src.utils.user.user_service import UserService


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

    async def create_communication_message_text(self, generated_text) -> List[MessageHistory]:
        return await self.save_to_database_message_history(
            new_user_message_history=[
                {"role": "user", "content": self.prompt},
                {"role": "assistant", "content": generated_text}
            ]
        )

    async def was_last_message_sent_two_days_ago(self) -> bool:
        user_history = await self.get_user_message_history()

        if user_history and user_history.user_message_history:
            last_message = user_history.user_message_history[-1]

            if last_message.created_at <= datetime.now() - timedelta(days=2):
                return True

        return False

    @Transactional()
    async def save_to_database_message_history(
            self,
            new_user_message_history: GetNewUserMessageHistory
    ) -> List[MessageHistory]:
        messages = [
            MessageHistory(
                tg_id=str(self.tg_id),
                message=row["content"],
                role=row["role"],
                type=self.type_message
            )
            for row in new_user_message_history
        ]
        for message in messages:
            session.add(message)
        return messages

    async def get_user_message_history(self) -> GetUserMessageHistory:
        return await UserService().get_user_message_history(tg_id=str(self.tg_id))
