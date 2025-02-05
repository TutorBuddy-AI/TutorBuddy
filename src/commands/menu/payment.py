from aiogram import types, md, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from src.config import bot
from src.config import config
from src.filters.is_not_register_filter import IsRegister, IsNotRegister
from src.keyboards import get_keyboard_remove
from src.utils.answer import AnswerRenderer
from src.utils.payments import PaymentHandler
from src.database.models.payment import Subscription, Order

from src.database import session
from sqlalchemy import select, desc
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

payment_router = Router(name=__name__)


#@payment_router.message(Command("subscription"))
#@payment_router.message(F.text.lower() == "subscription")
#async def process_subscription_handler(message: types.Message, state: FSMContext):
@payment_router.message(IsRegister(), Command("payment"))
async def process_payment_handler(message: types.Message):
#    current_state = await state.get_state()
#    if current_state is None:
#        return

#    await bot.send_message(message.chat.id, 'Subscription & Check Payments...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#    print(f"*** process_subscription_handler")

    tg_id = str(message.chat.id)
    await PaymentHandler.update_payments(tg_id)

##    result = await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='pending').order_by(desc(Order.created_at)))
##    orders = result.scalars().all()
#    orders = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='pending').order_by(desc(Order.created_at)))).scalars().all()
#    if orders:
#        for order in orders:
#            await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \npending order_id : {order.id} order.payment_id : {order.payment_id} order.product : {order.product}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#            payment_status = await PaymentHandler.payment_check(order.payment_id)
#            await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} current payment status : {payment_status}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#            if payment_status == 'waiting_for_capture':
#                await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} processing capture payment", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#                await PaymentHandler.payment_capture(order.payment_id)
#                payment_status = await PaymentHandler.payment_check(order.payment_id)
#                await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} payment status after capture : {payment_status}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
            # uncomment next line for test!
#        #    elif payment_status == 'succeeded':
#                if payment_status == 'succeeded':
#                    count_month = 0
#                    if order.product_id == 'subs1m':
#                        count_month = 1
#                    elif order.product_id == 'subs6m':
#                        count_month = 6

##                    start_date = datetime.strptime(order.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
#                    start_at = order.paid_at
#                    end_at = start_at + timedelta(days=int(count_month) * 30)

#                    new_subscription = Subscription(
#                        tg_id=tg_id,
#                        product_id=order.product_id,
#                        count_msg=0,
#                        count_mist=0,
#                        start_at=start_at,
#                        end_at=end_at,
#                    )
#                    session.add(new_subscription)
#                    await session.commit()
#                    await session.close()

#                    formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
#                    await bot.send_message(message.chat.id, f"🔥Вы успешно оплатили подписку. Следующий платёж {formatted_date}, tg_id: {tg_id}, count_month: {count_month}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#    else:
#        await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \npending orders not found", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

##    result = await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='succeeded').order_by(desc(Order.created_at)))
##    order = result.scalars().first()
#    order = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='succeeded').order_by(desc(Order.created_at)))).scalars().first()
#    if order:
#        await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \nsucceeded order_id : {order.id} order.product : {order.product}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#    else:
#        await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \nsucceeded order not found", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

##    result = await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).order_by(desc(Subscription.end_at)))
##    subscription = result.scalars().first()
#    subscription = (await session.execute(select(Subscription).where(Subscription.tg_id == tg_id).order_by(desc(Subscription.end_at)))).scalars().first()
#    if subscription:
#        await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \nsubscription found, product_id : {subscription.product_id} start_at : {subscription.start_at} end_at : {subscription.end_at}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#        current_time = datetime.now().astimezone(timezone.utc)
#        if (subscription.start_at <= current_time) and (subscription.end_at > current_time):
#            formatted_date = subscription.end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
#            if subscription.product_id.startswith('subs'):
#                await bot.send_message(message.chat.id, f"🔥У Вас есть активная подписка. Следующий платёж {formatted_date} tg_id: {tg_id}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#            else:
#                await bot.send_message(message.chat.id, f"🔥У Вас продолжается демо режим. Окончание {formatted_date} tg_id: {tg_id}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#    else:
#        await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \nsubscription not found", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
##        await PaymentHandler.send_payment_message(tg_id)

    result = await PaymentHandler.check_subscription(tg_id)
    if result == None:
        await PaymentHandler.send_payment_message(tg_id)


@payment_router.message(IsNotRegister(), Command("payment"))
async def process_payment_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text="Please, register first", parse_mode=ParseMode.HTML,
                           reply_markup=translate_markup)


@payment_router.message(IsRegister(), Command("start"))
async def process_start_handler(message: types.Message, command: CommandObject):
#    await bot.send_message(message.chat.id, 'Start test...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

    if command.args == None:
        await bot.send_message(message.chat.id, "Great!\nSend me message below ⬇", parse_mode=ParseMode.HTML,
                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))

    elif command.args == config.PAYMENT_DEMO_RESET_TAG:
        await bot.send_message(message.chat.id, 'Start with Demo Reset...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

        tg_id = str(message.chat.id)
        subscription = (await session.execute(
            select(Subscription)
            .where(Subscription.tg_id == tg_id)
            .where(Subscription.product_id.like('demo%'))
            .order_by(desc(Subscription.end_at)))
        ).scalars().first()

        if subscription:
            subscription.product_id = 'reset' + subscription.product_id[4:]
            await session.commit()

            await bot.send_message(tg_id, f"🔥Сброшена подписка для демо режима.", parse_mode=ParseMode.HTML)

    elif command.args == config.PAYMENT_FREE_10MIN_TAG:
        await bot.send_message(message.chat.id, 'Start with Free 10 Minutes Subscription...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

        tg_id = str(message.chat.id)
        result = await PaymentHandler.check_subscription(tg_id)
        if result == None:
            start_at = datetime.now()
            end_at = start_at + timedelta(minutes = 10)

            new_subscription = Subscription(
                tg_id=tg_id,
                product_id='free1m',
                count_msg=0,
                count_mist=0,
                start_at=start_at,
                end_at=end_at,
            )
            session.add(new_subscription)
            await session.commit()
            await session.close()

            formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
            await bot.send_message(tg_id, f"🔥Создана подписка для free 10 minutes режима. Окончание {formatted_date} tg_id: {tg_id}", parse_mode=ParseMode.HTML)

    elif command.args == config.PAYMENT_FREE_1MO_TAG:
        await bot.send_message(message.chat.id, 'Start with Free One Month Subscription...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

        tg_id = str(message.chat.id)
        result = await PaymentHandler.check_subscription(tg_id)
        if result == None:
            start_at = datetime.now()
            end_at = start_at + timedelta(minutes = config.PAYMENT_1MO_DURATION)

            new_subscription = Subscription(
                tg_id=tg_id,
                product_id='free1m',
                count_msg=0,
                count_mist=0,
                start_at=start_at,
                end_at=end_at,
            )
            session.add(new_subscription)
            await session.commit()
            await session.close()

            formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
            await bot.send_message(tg_id, f"🔥Создана подписка для free one month режима. Окончание {formatted_date} tg_id: {tg_id}", parse_mode=ParseMode.HTML)

    elif command.args == 'payments':
        await bot.send_message(message.chat.id, 'Start with Payments Check...', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

        tg_id = str(message.chat.id)
        await PaymentHandler.update_payments(tg_id)

##        result = await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='pending').order_by(desc(Order.created_at)))
##        orders = result.scalars().all()
#        orders = (await session.execute(select(Order).where(Order.tg_id == tg_id).filter_by(status='pending').order_by(desc(Order.created_at)))).scalars().all()
#        if orders:
#            for order in orders:
#                await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \npending order_id : {order.id} order.payment_id : {order.payment_id} order.product : {order.product}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#                payment_status = await PaymentHandler.payment_check(order.payment_id)
#                await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} current payment status : {payment_status}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#                if payment_status == 'waiting_for_capture':
#                    await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} processing capture payment", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#                    await PaymentHandler.payment_capture(order.payment_id)
#                    payment_status = await PaymentHandler.payment_check(order.payment_id)
#                    await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \norder_id : {order.id} payment status after capture : {payment_status}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
                # uncomment next line for test!
#            #    elif payment_status == 'succeeded':
#                    if payment_status == 'succeeded':
#                        count_month = 0
#                        if order.product_id == 'subs1m':
#                            count_month = 1
#                        elif order.product_id == 'subs6m':
#                            count_month = 6

#                        start_at = order.paid_at
#                        end_at = start_at + timedelta(days=int(count_month) * 30)

#                        new_subscription = Subscription(
#                            tg_id=tg_id,
#                            product_id=order.product_id,
#                            count_msg=0,
#                            count_mist=0,
#                            start_at=start_at,
#                            end_at=end_at,
#                        )
#                        session.add(new_subscription)
#                        await session.commit()
#                        await session.close()

#                        formatted_date = end_at.astimezone(ZoneInfo(config.TIME_ZONE)).strftime('%d-%m-%Y %H:%M')
#                        await bot.send_message(message.chat.id, f"🔥Вы успешно оплатили подписку. Следующий платёж {formatted_date}, tg_id: {tg_id}, count_month: {count_month}", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
#        else:
#            await bot.send_message(message.chat.id, f"*** tg_id : {tg_id} \npending orders not found", parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())

##    else:
##        await bot.send_message(message.chat.id, "Great!\nSend me message below ⬇", parse_mode=ParseMode.HTML,
##                               reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True))
##        current_state = await state.get_state()
##        if current_state is None:
##            return
##        await state.clear()
