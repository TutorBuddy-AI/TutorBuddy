import uuid
from yookassa import Payment
from src.database.models import User


def get_payment_url(amount, payload, desc, user: User) -> str:
    """
    Get youkassa payment url

    :param int amount: Price
    :param str payload: Payment object name (for subscription detect)
    :param str desc: Payment description
    :param User user: User object
    :return: payment url str
    """

    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "metadata": {
            "user_id": user.id,
            "payload": payload,
            "chat_id": user.history[-1].chat_id
        },
        "receipt": {
            "customer": {
                "full_name": user.get_full_name,
                "email": user.email
            },
            "items": [
                {
                    "description": desc,
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": "1",
                    "payment_mode": "full_payment",
                    "payment_subject": "service"
                }
            ]
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://glimmerai.tech"
        },
        "capture": True,
        "description": desc
    }, idempotence_key)

    return payment.confirmation.confirmation_url
