import uuid
from yookassa import Configuration, Payment
# from config.config import config
from src.config import bot, dp, config
import logging
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from src.database import session
from src.database.models.payment import Subscription, Order
from src.utils.stciker.sticker_sender import StickerSender
from src.utils.stciker.sticker_pack import pack_map
from sqlalchemy import select, desc, text, delete, Row, RowMapping, func
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

logging.basicConfig(
    filename="payment.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class PaymentHandler:
#    def __init__(self):
#        pass

    @staticmethod
    async def create_payment_url(tg_id: str, month: int):
        try:
            value = "0.00"
            if month == 1:
                value = config.PAYMENT_PRICE_1MO
            elif month == 6:
                value = config.PAYMENT_PRICE_6MO

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
                    "return_url": f"{config.PAYMENT_RETURN_URL}"
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

            new_order = Order(
                tg_id=tg_id,
                product_id=f"subs{month}m",
                product=f"Subscription for {month} {month_text}",
                provider="yookassa",
                payment_id=payment.id,
                account_id=payment.recipient.account_id,
                gateway_id=payment.recipient.gateway_id,
                test=False,
                amount=str(payment.amount.value),
                currency=payment.amount.currency,
                status=payment.status,
            )
            session.add(new_order)
            await session.commit()
#            await session.close()

            return confirmation_url
        except Exception as e:
            logging.error(f"Ошибка в create_payment_url: {str(e)}")

    @staticmethod
    async def payment_check(payment_id: str):
        Configuration.account_id = config.PAYMENT_ID
        Configuration.secret_key = config.PAYMENT_KEY
        payment = Payment.find_one(payment_id)

##        result = await session.execute(select(Order).where(Order.payment_id == payment_id).order_by(desc(Order.created_at)))
##        order = result.scalars().first()
        order = (await session.execute(select(Order).where(Order.payment_id == payment_id).order_by(desc(Order.created_at)))).scalars().first()

        if (order.status != payment.status) and (payment.status == 'succeeded') and (payment.paid == True):
#            order.paid_at = datetime.strptime(payment.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            order.paid_at = datetime.now()

        order.status = payment.status
        await session.commit()
#        await session.close()

        return payment.status

    @staticmethod
    async def payment_capture(payment_id: str):
        Configuration.account_id = config.PAYMENT_ID
        Configuration.secret_key = config.PAYMENT_KEY
        Payment.capture(payment_id)

    @staticmethod
    async def yookassa_handler(event_type: str, payment_id: str, tg_id: str, count_month: str, created_at:str):
        try:
            if "succeeded" in event_type:
                start_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                end_at = start_at + timedelta(days=int(count_month) * 30)

                new_subscription = Subscription(
                    tg_id=tg_id,
                    product_id=f"subs{count_month}m",
                    count_msg=0,
                    count_mist=0,
                    start_at=start_at,
                    end_at=end_at,
                )
                session.add(new_subscription)
                await session.commit()
#                await session.close()

                formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
                await bot.send_message(tg_id, f"Вы успешно оплатили подписку. Следующий платёж {formatted_date}, tg_id: {tg_id}, count_month: {count_month}", parse_mode=ParseMode.HTML)
                # await PaymentHandler.send_payment_message(int(tg_id)) # Вызов сообщения ссылками на оплату
        except Exception as e:
            logging.error(f"Ошибка в yookassa_handler: {str(e)}")

    @staticmethod
    async def send_payment_message(tg_id: str):
        try:
##            result = await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(product='Subscription for 1 month', status='pending').order_by(desc(Order.created_at)))
##            order = result.scalars().first()
            order = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(product_id='subs1m', status='pending').order_by(desc(Order.created_at)))).scalars().first()
            if order:
                url_1_month = f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={order.payment_id}"
            else:
                url_1_month = await PaymentHandler.create_payment_url(tg_id=tg_id, month=1)

##            result = await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(product='Subscription for 6 months', status='pending').order_by(desc(Order.created_at)))
##            order = result.scalars().first()
            order = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(product_id='subs6m', status='pending').order_by(desc(Order.created_at)))).scalars().first()
            if order:
                url_6_month = f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={order.payment_id}"
            else:
                url_6_month = await PaymentHandler.create_payment_url(tg_id=tg_id, month=6)

#            await bot.send_photo(
#                tg_id,
#                caption="You chatted enough today😓\n\n"
#                        "I want to keep talking 🤗\n\n"
#                        "Upgrade for more chat time! It's cheap, like just a few cups of coffee a month ☕️ ☕️ 😉\n\n"
#                        "⚡️ 1 month - 990₽\n"
#                        "🔥 6 month - 4900₽\n\n"
#                        "Subscribe 👇",
#                photo=FSInputFile('./files/payment.png'),
#                parse_mode=ParseMode.HTML,
#                reply_markup=PaymentHandler.keyboard_payment(url_1_month, url_6_month)
#            )
#            await bot.send_photo(
#                tg_id,
#                caption="На сегодня лимит истек (\n\n"
#                        "Подпишись и продолжим!\n"
#                        "Это не дорого, как пара чашек кофе в месяц ☕️ ☕️ 😉\n\n"
#                        "⚡️ 1 месяц - 1 390₽\n"
#                        "🔥 6 месяцев - 6 590₽\n",
#                photo=FSInputFile('./files/payment.png'),
#                parse_mode=ParseMode.HTML,
#                reply_markup=PaymentHandler.keyboard_payment(url_1_month, url_6_month)
#            )
#            sticker_sender = StickerSender(bot, tg_id, speaker=user_info["speaker"])
#            await sticker_sender.send_you_rock_sticker()
#            await bot.send_sticker(
#                tg_id,
#                "CAACAgIAAxkBAAErXGVmQONM_ItvhdEAAX0qDUS4VULKPzMAAkFHAALkhKlJibwQQwgywDk1BA",
#            )
#            await bot.send_message(
#                tg_id,
#                '<span class="tg-spoiler">😧 Ого, я этого не ожидала...</span>',
#                parse_mode=ParseMode.HTML
#            )
            await bot.send_message(
                tg_id,
                "На сегодня лимит истек (\n\n"
                "Подпишись и продолжим!\n"
                "Это не дорого, как пара чашек кофе в месяц ☕️ ☕️ 😉\n\n"
                "⚡️ 1 месяц - 1 390₽\n"
                "🔥 6 месяцев - 6 590₽\n",
                parse_mode=ParseMode.HTML,
                reply_markup=PaymentHandler.keyboard_payment(url_1_month, url_6_month)
            )
        except Exception as e:
            logging.error(f"Ошибка в send_payment_message: {str(e)}")

    @staticmethod
    def keyboard_payment(url_1_month: str, url_6_month: str):
        button_url_payment_1 = InlineKeyboardButton(text="⚡️ 1 month - 1 390₽", url=url_1_month)
        button_url_payment_6 = InlineKeyboardButton(text="🔥 6 month - 6 590₽", url=url_6_month)

        keyboard_payment = InlineKeyboardMarkup(inline_keyboard=[
            [button_url_payment_1, button_url_payment_6]
        ])
        return keyboard_payment

    @staticmethod
    async def update_payments(tg_id: str):
        try:
            orders = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='pending').order_by(desc(Order.created_at)))).scalars().all()
            if orders:
                for order in orders:
#                    await bot.send_message(tg_id, f"*** tg_id : {tg_id} \npending order_id : {order.id} order.payment_id : {order.payment_id} order.product : {order.product}", parse_mode=ParseMode.HTML)
                    payment_status = await PaymentHandler.payment_check(order.payment_id)
#                    await bot.send_message(tg_id, f"*** tg_id : {tg_id} \norder_id : {order.id} current payment status : {payment_status}", parse_mode=ParseMode.HTML)
                    if payment_status == 'waiting_for_capture':
#                        await bot.send_message(tg_id, f"*** tg_id : {tg_id} \norder_id : {order.id} processing capture payment", parse_mode=ParseMode.HTML)
                        await PaymentHandler.payment_capture(order.payment_id)
                        payment_status = await PaymentHandler.payment_check(order.payment_id)
#                        await bot.send_message(tg_id, f"*** tg_id : {tg_id} \norder_id : {order.id} payment status after capture : {payment_status}", parse_mode=ParseMode.HTML)
                    # uncomment next line for test!
#                    elif payment_status == 'succeeded':
                        if payment_status == 'succeeded':
                            count_month = 0
                            if order.product_id == 'subs1m':
                                count_month = 1
                            elif order.product_id == 'subs6m':
                                count_month = 6

##                            start_date = datetime.strptime(order.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
                            start_at = order.paid_at
#                            end_at = start_at + timedelta(days=int(count_month) * 30)
                            end_at = start_at + timedelta(minutes=int(count_month) * config.PAYMENT_1MO_DURATION)

                            new_subscription = Subscription(
                                tg_id=tg_id,
                                product_id=order.product_id,
                                count_msg=0,
                                count_mist=0,
                                start_at=start_at,
                                end_at=end_at,
                            )
                            session.add(new_subscription)
                            await session.commit()
                            await session.close()

                            formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
#                            await bot.send_message(tg_id, f"🔥Вы успешно оплатили подписку. Следующий платёж {formatted_date}, tg_id: {tg_id}, count_month: {count_month}", parse_mode=ParseMode.HTML)
                            await bot.send_message(tg_id, f"🔥Вы успешно оплатили подписку. Следующий платёж {formatted_date}\n\nGreat ! Let's keep chatting 😉", parse_mode=ParseMode.HTML)
#            else:
#                await bot.send_message(tg_id, f"*** tg_id : {tg_id} \npending orders not found", parse_mode=ParseMode.HTML)

        except Exception as e:
            logging.error(f"Ошибка в update_payments: {str(e)}")

    @staticmethod
    async def check_subscription(tg_id: str, flag_msg=None, flag_mist=None):
        try:
            subscription = (await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).where(Subscription.product_id.like('demo%')).order_by(desc(Subscription.end_at)))).scalars().first()
            if not subscription:
#                await bot.send_message(tg_id, f"*** tg_id : {tg_id} \ndemo subscription not found", parse_mode=ParseMode.HTML)

                start_at = datetime.now()
#                end_at = start_at + timedelta(days=2)
                end_at = start_at + timedelta(minutes = config.PAYMENT_DEMO_DURATION)

                new_subscription = Subscription(
                    tg_id=tg_id,
                    product_id='demo2d',
                    count_msg=0,
                    count_mist=0,
                    start_at=start_at,
                    end_at=end_at,
                )
                session.add(new_subscription)
                await session.commit()
                await session.close()

                formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
#                await bot.send_message(tg_id, f"🔥Создана подписка для демо режима. Окончание {formatted_date}, tg_id: {tg_id}", parse_mode=ParseMode.HTML)
                await bot.send_message(tg_id, f"🔥Создана подписка для демо режима. Окончание {formatted_date}", parse_mode=ParseMode.HTML)

#            else:
#                await bot.send_message(tg_id, f"*** tg_id : {tg_id} \ndemo subscription found", parse_mode=ParseMode.HTML)

##            result = await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).order_by(desc(Subscription.end_at)))
##            subscription = result.scalars().first()
            subscription = (await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).order_by(desc(Subscription.end_at)))).scalars().first()
            if subscription:
#                await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nsubscription found, product_id : {subscription.product_id} start_at : {subscription.start_at} end_at : {subscription.end_at}", parse_mode=ParseMode.HTML)
                current_time = datetime.now().astimezone(timezone.utc)
                if (subscription.start_at <= current_time) and (subscription.end_at > current_time):
                    formatted_date = subscription.end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
                    if subscription.product_id.startswith('subs'):
#                        await bot.send_message(tg_id, f"🔥У Вас есть активная подписка. Следующий платёж {formatted_date}, tg_id: {tg_id}", parse_mode=ParseMode.HTML)
                        await bot.send_message(tg_id, f"🔥У Вас есть активная подписка. Следующий платёж {formatted_date}", parse_mode=ParseMode.HTML)
                    elif subscription.product_id.startswith('free'):
#                        await bot.send_message(tg_id, f"🔥У Вас продолжается free режим. Окончание {formatted_date}, tg_id: {tg_id}", parse_mode=ParseMode.HTML)
                        await bot.send_message(tg_id, f"🔥У Вас продолжается free режим. Окончание {formatted_date}", parse_mode=ParseMode.HTML)
                    else:
#                        await bot.send_message(tg_id, f"🔥У Вас продолжается демо режим. Окончание {formatted_date}, tg_id: {tg_id}", parse_mode=ParseMode.HTML)
                        await bot.send_message(tg_id, f"🔥У Вас продолжается демо режим. Окончание {formatted_date}", parse_mode=ParseMode.HTML)
                    return subscription
                else:
                    subscription = (await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).where(Subscription.product_id.like('demo%')).order_by(desc(Subscription.end_at)))).scalars().first()
                    if not subscription:
#                        await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nold demo subscription not found", parse_mode=ParseMode.HTML)
                        return None
                    else:
#                        await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nold demo subscription found", parse_mode=ParseMode.HTML)

                        current_time = datetime.now().astimezone(timezone.utc)
#                        if (subscription.updated_at + timedelta(days=1)) < current_time:
                        if (subscription.updated_at + timedelta(minutes = config.PAYMENT_FREE_RESET_DURATION)) < current_time:
                            subscription.count_msg = 0
                            subscription.count_mist = 0
                            await session.commit()
#                            await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nthe counters have been cleared", parse_mode=ParseMode.HTML)

                        if flag_msg and (subscription.count_msg < config.PAYMENT_FREE_MSG):
                            subscription.count_msg += 1
                            await session.commit()
#                            await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nmsg counter incremented, you have a few more attempts", parse_mode=ParseMode.HTML)
                            return session
                        elif flag_msg:
#                            await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nmsg attempts is over", parse_mode=ParseMode.HTML)
                            return None

                        if flag_mist and (subscription.count_mist < config.PAYMENT_FREE_MIST):
                            subscription.count_mist += 1
                            await session.commit()
#                            await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nmist counter incremented, you have a few more attempts", parse_mode=ParseMode.HTML)
                            return session
                        elif flag_mist:
#                            await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nmist attempts is over", parse_mode=ParseMode.HTML)
                            return None

                        return None
            else:
#                await bot.send_message(tg_id, f"*** tg_id : {tg_id} \nsubscription not found", parse_mode=ParseMode.HTML)
                return None

            return None

        except Exception as e:
            logging.error(f"Ошибка в check_subscription: {str(e)}")
