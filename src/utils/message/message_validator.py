TEXT_MAX_SIZE: int = 4096
CAPTION_MAX_SIZE: int = 1024


async def get_text_token_size(text_length: int) -> int:
    return TEXT_MAX_SIZE - text_length


async def get_caption_token_size(text_length: int) -> int:
    return CAPTION_MAX_SIZE - text_length


def get_text_size_valid(text_length: int) -> bool:
    return text_length > TEXT_MAX_SIZE // 2


def get_caption_size_valid(text_length: int) -> bool:
    return text_length > CAPTION_MAX_SIZE // 2
