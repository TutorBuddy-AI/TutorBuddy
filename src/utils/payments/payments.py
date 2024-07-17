import uuid
from yookassa import Configuration, Payment
# from config.config import config
from src.config import bot, dp
import logging
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile,InlineKeyboardButton, InlineKeyboardMarkup



logging.basicConfig(
    filename="payment.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class PaymentHandler:
    @staticmethod
    async def create_payment_url(tg_id: str, month: int):
        try:
            value = "0.00"
            if month == 1:
                value = "10.00"
            elif month == 6:
                value = "16.00"

            month_text = "month" if month == 1 else "months"

            Configuration.account_id = PAYMENT_ID
            Configuration.secret_key = PAYMENT_KEY

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
        except Exception as e:
            logging.error(f"Ошибка в create_payment_url: {str(e)}")

    @staticmethod
    async def payment_check(payment_id: str):
        Configuration.account_id = PAYMENT_ID
        Configuration.secret_key = PAYMENT_KEY
        payment = Payment.find_one(payment_id)
        return payment.status

    @staticmethod
    async def payment_capture(payment_id: str):
        Configuration.account_id = PAYMENT_ID
        Configuration.secret_key = PAYMENT_KEY
        Payment.capture(payment_id)

    @staticmethod
    async def yookassa_handler(event_type: str, payment_id: str, tg_id: str, count_month: str):
        try:
            if "succeeded" in event_type:
                await bot.send_message(tg_id, f"tg_id: {tg_id}, count_month: {count_month}",parse_mode=ParseMode.HTML,)
                # await PaymentHandler.send_payment_message(int(tg_id)) # Вызов сообщения ссылками на оплату
        except Exception as e:
            logging.error(f"Ошибка в yookassa_handler: {str(e)}")

    @staticmethod
    async def send_payment_message(tg_id: str):
        try:
            url_1_month = await PaymentHandler.create_payment_url(tg_id=tg_id, month=1)
            url_6_month = await PaymentHandler.create_payment_url(tg_id=tg_id, month=6)
            await bot.send_photo(
                tg_id,
                caption="You chatted enough today😓\n\n"
                        "I want to keep talking 🤗\n\n"
                        "Upgrade for more chat time! It's cheap, like just a few cups of coffee a month ☕️ ☕️ 😉\n\n"
                        "⚡️ 1 month - 990₽\n"
                        "🔥 6 month - 4900₽\n\n"
                        "Subscribe 👇",
                photo=FSInputFile('./files/payment.png'),
                parse_mode=ParseMode.HTML,
                reply_markup=PaymentHandler.keyboard_payment(url_1_month, url_6_month)
            )
        except Exception as e:
            logging.error(f"Ошибка в send_payment_message: {str(e)}")

    @staticmethod
    def keyboard_payment(url_1_month: str, url_6_month: str):
        button_url_payment_1 = InlineKeyboardButton(text="⚡ 1 month - 990₽", url=url_1_month)
        button_url_payment_6 = InlineKeyboardButton(text="🔥 6 month - 4900₽", url=url_6_month)

        keyboard_payment = InlineKeyboardMarkup(inline_keyboard=[
            [button_url_payment_1, button_url_payment_6]
        ])
        return keyboard_payment
