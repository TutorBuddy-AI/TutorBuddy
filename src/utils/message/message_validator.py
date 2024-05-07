TEXT_MAX_SIZE: int = 4096
CAPTION_MAX_SIZE: int = 1024


async def get_text_token_size(text_length: int) -> int:
    return TEXT_MAX_SIZE - text_length


async def get_caption_token_size(text_length: int) -> int:
    return CAPTION_MAX_SIZE - text_length
