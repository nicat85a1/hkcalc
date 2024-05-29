from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CoinData
from django.contrib.auth.models import User

@receiver(post_save, sender=CoinData)
def add_default_coin_to_users(sender, instance, created, **kwargs):
    if created and instance.is_default:
        users = User.objects.all()
        for user in users:
            CoinData.objects.create(
                user=user,
                coin_name=instance.coin_name,
                sbk_value=instance.sbk_value,
                price=instance.price,
                is_default=False  # Kullanıcı için varsayılan coini işaretlemiyoruz
            )
