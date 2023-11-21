from src.utils.user import UserService
from src.utils.generate import GenerateAI
from src.database.models import MessageHistory
from src.database import Transactional, session

class UserCreateMessage:
    def __init__(self):
        ...

    @Transactional()
    async def create_message_user(
            self,
            tg_id: str,
            prompt: str,
            type_message: str
    ) -> str:
        user_message_history = await UserService().get_user_message_history(tg_id=str(tg_id))

        result = await GenerateAI(prompt=prompt).generate_text(user_message_history, tg_id)

        try:
            result["message"][0]["message"] = result["message"][0]["message"].split("±")[1]
            new_user_message_history = result["message"]

            generated_text = result["generated_text"]

        except:
            return "Oooops, repeat the request again"

        for row in new_user_message_history:
            message_history = MessageHistory(
                tg_id=str(tg_id),
                message=row["message"],
                role=row["role"],
                type=type_message
            )

            session.add(message_history)

         # Тут списывать кредиты (если так нужно будет :) )

        return generated_text
