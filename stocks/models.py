from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    # name = models.CharField(max_length=255)

    def __str__(self):
        return self.symbol
    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    stocks = models.ManyToManyField(Stock, related_name='watchlists')

    def __str__(self):
        return f"{self.user.username}'s Watchlist"