# from django.apps import AppConfig
#
#
# class QuanlybaivietConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'quanlybaiviet'
from django.apps import AppConfig


class QuanlybaivietConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quanlybaiviet'

    def ready(self):
        # Import signals
        import quanlybaiviet.signals
