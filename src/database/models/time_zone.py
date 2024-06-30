# import pytz
# from tzwhere import tzwhere
# from src.database.models.user import UserLocation
#
# def get_timezone(city):
#     tz = tzwhere.tzwhere()
#     coordinates = tz.findtz(lat=0, lng=0)
#     timezone_str = tz.tzNameAt(coordinates[0], coordinates[1], forceTZ=True)
#     timezone = pytz.timezone(timezone_str)
#     return timezone
#
# async def update_user_timezone(tg_id, city):
#     timezone = get_timezone(city)
#     async with async_session_factory() as session:
#         user_location = await session.get(UserLocation, tg_id)
#         if user_location:
#             user_location.time_zone = str(timezone)
#             await session.commit()
