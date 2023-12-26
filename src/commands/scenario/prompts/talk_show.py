class TalkShowPrompt:
    def __init__(self, job: str):
        self.job = job

    async def get_introduction(self) -> str:
        return f"Сreate a script for a talk show where I will be interviewing a famous {self.job}"

    async def get_question(self, previous_questions: str = "") -> str:
        return f"Please write one question that a tv show host can ask his celebrity guest if he is a {self.job}." \
               f"You can't repeat yourself. Previous questions were: {previous_questions}"

    async def get_question_future(self, previous_questions: str = "") -> str:
        return f"Please write a one question about the future of a career that a TV show host might ask his celebrity" \
               f" guest if he {self.job}. You can't repeat yourself. Previous questions were: {previous_questions}"

    async def get_question_advice_to_newcomers(self, previous_questions: str = "") -> str:
        return f"Please write the one question “what advice would you give to newcomers” that a TV show host could ask his" \
               f" celebrity guest if he {self.job}. You can't repeat yourself." \
               f" Previous questions were: {previous_questions}"

    async def get_end(self) -> str:
        return f"Please write a text in which you say goodbye and thank you, which the TV show host can ask his" \
               f" celebrity guest if he {self.job}."
