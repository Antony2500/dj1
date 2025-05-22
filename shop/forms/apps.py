from django.apps import AppConfig


class FormsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forms'

class MyAppConfig(AppConfig):
    name = "myapp"
    def ready(self):
        # важливо: імпорт всередині ready()
        import signals