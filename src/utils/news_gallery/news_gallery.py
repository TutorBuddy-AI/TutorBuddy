import html
import traceback
from datetime import date
from typing import List, Optional

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

from src.config import bot
from src.utils.answer import AnswerRenderer
from src.utils.generator.news_greetings_generator.talk_initializer import NewsGreetingsGenerator
from src.utils.newsletter.newsletter_service import NewsletterService
from src.utils.newsletter.schema.newsletter import UserNewsSummary, NewsletterGaleryPreview


class GalleryButtonClickData(CallbackData, prefix="gallery_scroll"):
    action: str
    topics: str
    target_date: date
    newsletter_index: int
    num_newsletters: int


num_topics_map = {str(num): topic for num, topic in
                  enumerate(["psychology", "business", "startups", "innovations", "fashion", "health"])}


def topics_encode(list_topics: List[str]) -> List[str]:
    reversed_topics_map = {topic: num for num, topic in num_topics_map.items()}
    return [reversed_topics_map[key] for key in list_topics]


def topics_decode(list_encoded_topics: List[str]) -> List[str]:
    return [num_topics_map[key] for key in list_encoded_topics]


class NewsletterChoiceData(CallbackData, prefix="gallery_choose"):
    newsletter_index: int


class NewsGallery:
    async def send_news_gallery(self):
        user_galleries = await NewsletterService.get_fresh_user_topics_and_preview(date.today())
        for user_news_summary, gallery_preview in user_galleries:
            try:
                await self.send_news_gallery_greetings(user_news_summary)
                await self.send_user_gallery(user_news_summary, gallery_preview)
            except Exception as e:
                traceback.print_exc()

    async def send_news_gallery_greetings(self, user_news_summary: UserNewsSummary):
        greetings_text = await NewsGreetingsGenerator().generate_message()

        await bot.send_message(
            chat_id=int(user_news_summary.tg_id),
            text=greetings_text,
            parse_mode=ParseMode.HTML,
            reply_markup=AnswerRenderer.get_markup_text_translation_standalone()
        )

    async def send_user_gallery(self, user_news_summary: UserNewsSummary, gallery_preview: NewsletterGaleryPreview):
        if (user_news_summary is not None) and (user_news_summary.num_newsletters != 0):
            current_index = 0

            await NewsGallery.send_data(
                int(user_news_summary.tg_id), gallery_preview,
                NewsGallery.create_inline_keyboard(
                    user_news_summary.topics, date.today(),
                    current_index, user_news_summary.num_newsletters,
                    gallery_preview.id
                ))

    @staticmethod
    async def send_data(
            chat_id: int, data_element: Optional[NewsletterGaleryPreview],
            keyboard: InlineKeyboardMarkup, message_id=None):
        if message_id:
            if data_element is None:
                await bot.edit_message_media(
                    media=InputMediaPhoto(
                        media=types.FSInputFile('./files/404_not_found.jpg'),
                        caption="Looks like this newsletter was deleted",
                        parse_mode=ParseMode.HTML
                    ),
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=keyboard,
                )
            else:
                await bot.edit_message_media(
                    media=InputMediaPhoto(
#                        media=types.FSInputFile(data_element.img),
                        media=data_element.img,
                        caption=NewsGallery.formatting_post_text(data_element),
                        parse_mode=ParseMode.HTML
                    ),
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=keyboard,
                )
        else:
#            print(f"*** data_element.img: {data_element.img}")
            await bot.send_photo(
                chat_id=chat_id,
#                photo=types.FSInputFile(data_element.img),
                photo=data_element.img,
                caption=NewsGallery.formatting_post_text(data_element),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard)

    @staticmethod
    def formatting_post_text(newsletter) -> str:
        post_text = f"#dailysummaries\n#{newsletter.topic}\n\n"
        post_text += f"<b>{newsletter.title}</b>"

        if newsletter.publisher:
            post_text += f"\n{newsletter.publisher}"
        if newsletter.publication_date:
            post_text += f"\n{newsletter.publication_date}"

        post_text += "\n\n<u>Article summary:</u>"
        post_text += f"\n{newsletter.short_content}..."
        # Заменяем <br> на \n
        formatting_post_text = html.unescape(post_text.replace('<br>', ''))
        return formatting_post_text

    @staticmethod
    def create_inline_keyboard(
            topics: List[str], target_date: date.today(), gallery_index: int, total_elements: int,
            curr_newsletter_id: int, is_active=True):
        prev_button = InlineKeyboardButton(
            text="⬅️",
            callback_data=GalleryButtonClickData(
                action="prev",
                topics=",".join(topics_encode(topics)),
                target_date=target_date,
                newsletter_index=gallery_index,
                num_newsletters=total_elements
            ).pack())

        index_button = InlineKeyboardButton(text=f"{gallery_index + 1} / {total_elements}", callback_data="...........")

        next_button = InlineKeyboardButton(
            text="➡️",
            callback_data=GalleryButtonClickData(
                action="next",
                topics=",".join(topics_encode(topics)),
                target_date=target_date,
                newsletter_index=gallery_index,
                num_newsletters=total_elements
            ).pack())

        discuss_button = InlineKeyboardButton(
            text="Read and discuss 🔽📃",
            callback_data=NewsletterChoiceData(
                newsletter_index=curr_newsletter_id
            ).pack())

        go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

        if is_active:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[discuss_button], [prev_button, index_button, next_button], [go_back_btn]])
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[prev_button, index_button, next_button], [go_back_btn]])

        return keyboard
