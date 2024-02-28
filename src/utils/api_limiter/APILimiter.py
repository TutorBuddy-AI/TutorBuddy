from asyncio import Lock, Event
from typing import List


class APILimiter:
    def __init__(self, token):
        self.token = token

        self.tts_lock = Lock()
        self.tts_waiting_event = Event()
        self.tts_waiting_event.set()

        self.gpt3_lock = Lock()
        self.gpt3_waiting_event = Event()
        self.gpt3_waiting_event.set()

        self.stt_lock = Lock()
        self.stt_waiting_event = Event()
        self.stt_waiting_event.set()


def init_api_limitters(api_tokens: List[str]) -> List[APILimiter]:
    limiters = []
    for token in api_tokens:
        limiters.append(APILimiter(token))
    return limiters
