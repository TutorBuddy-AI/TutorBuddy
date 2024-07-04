CITY_TIMEZONES = [
    ('Лондон (UTC+1)', 'Лондон', 'utc01'),
    ('Калининград (UTC+2)', 'Калининград', 'timezone_utc02'),
    ('Мск - Спб (UTC+3)', 'Мск - Спб', 'utc03'),
    ('Уфа (UTC+5)', 'Уфа', 'utc05'),
    ('Красноярск (UTC+7)', 'Красноярск', 'utc07'),
    ('Владивосток (UTC+10)', 'Владивосток', 'utc10')
]


def get_timezone_city_mapping():
    return {timezone: city for _, city, timezone in CITY_TIMEZONES}
