from django.db import models
from django.contrib.auth.models import User

class CoinData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_name = models.CharField(max_length=100)
    sbk_value = models.FloatField()
    price = models.FloatField()
    is_default = models.BooleanField(default=False)  # Varsayılan verileri belirlemek için

    def __str__(self):
        return self.coin_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_request_limit = models.IntegerField(default=10)  # default limit is 10

    def __str__(self):
        return f"{self.user.username}'s profile"