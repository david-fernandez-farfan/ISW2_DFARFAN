from django.contrib.auth.models import User
from relecloud.services.purchases import user_has_purchased

def has_purchased(self, destination=None, cruise=None):
    return user_has_purchased(self, destination, cruise)

User.add_to_class("has_purchased", has_purchased)
