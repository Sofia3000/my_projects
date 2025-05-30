from django.contrib import admin

# Register your models here.
from .models import Category, Auction, Comment, Rate

admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Rate)



