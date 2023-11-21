import aiohttp

from src.utils.user.schemas import UserLocationInfo

class UserLocation:
    def __init__(self):
        ...

    async def get_user_location_info(self, ip_address: str) -> UserLocationInfo:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://freeipapi.com/api/json/{ip_address}") as response:
                if response.status == 200:
                    return await response.json()

                else:
                    return
