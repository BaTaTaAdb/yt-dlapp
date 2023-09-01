from django.apps import AppConfig


class VideosManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos_manager'

    def ready(self):
        import videos_manager.signals
