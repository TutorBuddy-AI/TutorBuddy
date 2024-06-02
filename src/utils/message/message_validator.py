TEXT_MAX_SIZE: int = 4096
CAPTION_MAX_SIZE: int = 1024


def get_text_size_valid(text_length: int) -> bool:
    return text_length < TEXT_MAX_SIZE


def get_caption_size_valid(text_length: int) -> bool:
    return text_length < CAPTION_MAX_SIZE
