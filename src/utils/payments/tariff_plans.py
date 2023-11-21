def get_available_models():
    return ['gpt-3.5-turbo', 'gpt-3.5-turbo-0301',
            'gpt-4', 'gpt-4-32k',
            'chat-bison',
            'falcon-40b', 'falcon-7b', 'llama-13b',
            'midjourney', 'stabilityai', 'dalle2', 'muse']


def get_tariff_plans():
    return {
        "free": {
            "purchased_images": 3,
            "credits": 10,
            "allowed_models": ["gpt-3.5-turbo", "dalle2"],
        },
        "starter": {
            "purchased_images": 10,
            "credits": 100,
            "allowed_models": ["gpt-3.5-turbo", "gpt-3.5-turbo-0301",
                               "gpt-4", "falcon-40b", "llama-13b", "dalle2", 'muse'],
        },
        "pro": {
            "purchased_images": 20,
            "credits": 200,
            "allowed_models": get_available_models(),
        }
    }
