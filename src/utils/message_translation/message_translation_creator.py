from utils.generate.translate.translate import TranslateGenerate


class MessageTranslationCreator:
    def __init__(
            self,
            tg_id: str,
            message: str
    ):
        self.tg_id = tg_id
        self.message = message

    async def create_communication_message_text(self) -> str:
        generated_text = await TranslateGenerate(
            tg_id=str(self.tg_id),
            en_string=self.message
        ).translate()

        if generated_text is not None:
            return generated_text
        else:
            return "Oooops, something wrong. Try request again later..."
