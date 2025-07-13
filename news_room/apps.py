# news_room/apps.py

from django.apps import AppConfig

class NewsRoomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_room'

    def ready(self):
        import news_room.signals 
