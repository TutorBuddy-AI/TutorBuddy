from pydantic import BaseModel

class GetUserInfo(BaseModel):
    name: str | None
    goal: str | None
    native_lang: str | None
    topic: str | None
    english_level: str | None

class UserInfo(BaseModel):
    tg_id: str
    call_name: str | None
    phone_number: str = None
    tg_firstName: str | None
    tg_lastName: str | None
    tg_language: str | None
    tg_username: str | None
    source: str | None
    goal: str | None
    native_lang: str | None
    topic: str | None
    english_level: str | None


class UserLocationInfo(BaseModel):
    ipAddress: str | None
    latitude: str | None
    longitude: str | None
    countryName: str | None
    countryCode: str | None
    timeZone: str | None
    zipCode: str | None
    cityName: str | None
    regionName: str | None
    continent: str | None
    continentCode: str | None


class StateUserInfo(BaseModel):
    name: str | None
    native_language: str | None
    goal: str | None
    english_level: str | None
    topic: str | None
    source: str | None
