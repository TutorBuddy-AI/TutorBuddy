from typing import Optional, List


class Answer:
    """Class, that provides the result of GPT generation"""
    def __init__(self, answer_text: Optional[str], mistakes: Optional[List[str]]):
        self.answer_text = answer_text
        self.mistakes = mistakes

        self.are_mistakes_provided = True if mistakes is not None else False
