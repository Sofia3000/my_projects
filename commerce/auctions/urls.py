from django.urls import path

from . import views

# import settings and static first
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newauction", views.create_auction, name="newauction"),
    path("auction/<int:id>", views.watch_auction, name="auction"),
    path("change_watchlist", views.change_watchlist, name="change_watchlist"),
    path("new_rate", views.new_rate, name="new_rate"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("new_comment", views.new_comment, name="new_comment"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("category_list", views.category_list, name="category_list"),
    path("category<int:id>", views.category, name="category")
]
