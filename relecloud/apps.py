from django.apps import AppConfig

def ready(self):
    import relecloud.services.attach_user_methods

class RelecloudConfig(AppConfig):
    name = 'relecloud'
