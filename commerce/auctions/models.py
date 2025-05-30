from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', related_name="watchers", blank=True)

class Category(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return f"{self.name}"
        
class Auction(models.Model):
    name = models.CharField(max_length=60)
    review = models.CharField(max_length=200)
    start_rate = models.DecimalField(max_digits=20, decimal_places=2, validators=(MinValueValidator(0.0),))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions", blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="auctions_images")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    isactive = models.BooleanField(default=True)

class Rate(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates")
    price = models.DecimalField(max_digits=20, decimal_places=2)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=300)

