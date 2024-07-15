import uuid
from yookassa import Configuration, Payment
from config.config import config
from src.config import bot, dp
import logging
from aiogram.enums import ParseMode

logging.basicConfig(
    filename="payment.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class PaymentHandler:
    @staticmethod
    async def create_payment(month, tg_id):
        value = "0.00"
        if month == 1:
            value = "10.00"
        elif month == 6:
            value = "16.00"

        month_text = "month" if month == 1 else "months"

        Configuration.account_id = config.PAYMENT_ID
        Configuration.secret_key = config.PAYMENT_KEY

        idempotence_key = str(uuid.uuid4())

        payment_data = {
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/testpaymentkassaru_bot/"
            },
            "description": f"{tg_id}",
            "receipt": {
                "customer": {
                    "email": "customer@example.com"
                },
                "items": [
                    {
                        "description": f"Subscription for {month} {month_text}",
                        "quantity": "1.00",
                        "amount": {
                            "value": value,
                            "currency": "RUB"
                        },
                        "vat_code": "1"
                    }
                ]
            }
        }

        payment = Payment.create(payment_data, idempotence_key)
        confirmation_url = payment.confirmation.confirmation_url
        return confirmation_url

    @staticmethod
    async def payment_check(payment_id):
        Configuration.account_id = config.PAYMENT_ID
        Configuration.secret_key = config.PAYMENT_KEY
        payment = Payment.find_one(payment_id)
        return payment.status

    @staticmethod
    async def payment_capture(payment_id):
        Configuration.account_id = config.PAYMENT_ID
        Configuration.secret_key = config.PAYMENT_KEY
        Payment.capture(payment_id)

    @staticmethod
    async def yookassa_handler(event_type, payment_id, tg_id, count_month):
        try:
            if "succeeded" in event_type:
                await bot.send_message(tg_id, f"Cool {tg_id}, count_month {count_month}", parse_mode=ParseMode.HTML, )
        except Exception as e:
            logging.error(e)
