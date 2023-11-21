import enum


class SubscriptionPlan(enum.Enum):
    free = "free"
    starter = "starter"
    pro = "pro"

class SubscriptionInterval(enum.Enum):
    month = "month"

class SubscriptionCurrency(enum.Enum):
    rub = "rub"
    usd = "usd"

class UserHistoryRequestType(enum.Enum):
    text = "text"
    image = "image"