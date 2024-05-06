from datetime import date

from aiogram.filters import Command

from admin.newsletter_admin.newsletter_admin import NewsletterPublisher
from filters.is_not_register_filter import IsRegister

from src.config import bot

from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.enums.parse_mode import ParseMode

from utils.news_gallery.news_gallery import NewsGallery, GalleryButtonClickData, NewsletterChoiceData
from utils.newsletter.newsletter_service import NewsletterService
from aiogram import Router

news_gallery_router = Router(name=__name__)


@news_gallery_router.message(IsRegister(), Command("news_gallery"))
async def get_news_gallery(message: types.Message, state: FSMContext):
    user_news_summary = await NewsletterService.get_fresh_user_topics_for_one_in_date(
        tg_id=str(message.chat.id),
        target_date=date.today()
    )
    if (user_news_summary is None) or (user_news_summary.num_newsletters == 0):
        await bot.send_message(message.chat.id,
                               text="I don't have any fresh news for you",
                               parse_mode=ParseMode.HTML)
    else:
        current_index = 0
        curr_newsletter_preivew = await NewsletterService.get_topics_newsletter_preview_on_date(
            user_news_summary.topics, date.today(), current_index)

        await NewsGallery.send_data(
            message.chat.id, curr_newsletter_preivew,
            NewsGallery.create_inline_keyboard(
                user_news_summary.topics, date.today(),
                current_index, user_news_summary.num_newsletters, curr_newsletter_preivew.id
            ))


@news_gallery_router.callback_query(GalleryButtonClickData.filter())
async def handle_inline_buttons(callback_query: types.CallbackQuery, callback_data: GalleryButtonClickData):
    num_news = callback_data.num_newsletters
    if num_news == 1:
        return
    current_index = callback_data.newsletter_index

    if callback_data.action == "prev":
        current_index = (current_index - 1) % num_news  # if current_index != 0 else num_news - 1
    elif callback_data.action == "next":
        current_index = (current_index + 1) % num_news

    topics = callback_data.topics.split(",")
    curr_newsletter_preivew = await NewsletterService.get_topics_newsletter_preview_on_date(
        topics, callback_data.target_date, current_index)

    message_id = callback_query.message.message_id

    await NewsGallery.send_data(
        callback_query.message.chat.id, curr_newsletter_preivew,
        NewsGallery.create_inline_keyboard(
            topics, callback_data.target_date, current_index, num_news, curr_newsletter_preivew.id),
        message_id)


@news_gallery_router.callback_query(NewsletterChoiceData.filter())
async def handle_inline_buttons(callback_query: types.CallbackQuery, callback_data: NewsletterChoiceData):
    newsletter_id = callback_data.newsletter_index
    newsletter = await NewsletterService.get_newsletter(newsletter_id)
    newsletter_audio_files = await NewsletterService.get_newsletter_audio_files(newsletter_id)
    await NewsletterPublisher().send_summary_and_opinion_to_chat(
        str(callback_query.message.chat.id), newsletter, newsletter_audio_files)
