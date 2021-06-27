#wechat chatbot
import redis
from django.conf import settings
from werobot import WeRoBot
from werobot.session.redisstorage import RedisStorage
from config.settings.base import env


db = redis.Redis(settings.REDIS_URL)
session_storage = RedisStorage(db, prefix="wxbot_")
wxbot = WeRoBot(
            token=env('WXBOT_TOKEN'),
            enable_session=True,
            session_storage=session_storage
        )

@wxbot.text
def handle_text(message, session):
    return ''


@wxbot.image
def handle_img(message, session):
    img = message.img
    return ''
