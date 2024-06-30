from src.database.models.user import User, UserLocation, Role, user_roles
from src.database.models.person import Person
from src.database.models.setting import Setting
from src.database.models.message_history import MessageHistory
from src.database.models.daily_news import DailyNews
from src.database.models.message_mistakes import MessageMistakes
from src.database import Base
from src.database.models.feedbacks_history import FeedbacksHistory
from src.database.models.questions_history import QuestionsHistory
from src.database.models.message_hint import MessageHint
from src.database.models.message_paraphrase import MessageParaphrase
from src.database.models.message_translation import MessageTranslation
from src.database.models.message_for_users import MessageForUsers
from src.database.models.admin import Admin
# from src.database.models.time_zone import update_user_timezone