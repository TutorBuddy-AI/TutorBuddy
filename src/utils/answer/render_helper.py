from aiogram.dispatcher import FSMContext

from utils.answer.render import Render


class RenderHelper:
    def __init__(self, state: FSMContext):
        self.state = state

    async def group_render_info(
            self) -> Render:
        state_data = await self.state.get_data()
        render = Render(
            answer_text = state_data["answer_text"],
            is_generation_successful = state_data["is_generation_successful"],
            user_message_markup = state_data["user_message_markup"],
            bot_message_markup = state_data["bot_message_markup"],
            message_text = state_data["message_text"],
            message_type = state_data["message_type"]
        )
        return render

    async def save_render_info(
            self, render: Render):
        state_data = await self.state.get_data()
        state_data["answer_text"] = render.answer_text
        state_data["is_generation_successful"] = render.is_generation_successful
        state_data["user_message_markup"] = render.user_message_markup
        state_data["bot_message_markup"] = render.bot_message_markup
        state_data["message_text"] = render.message_text
        state_data["message_type"] = render.message_type
        await self.state.update_data(state_data)