from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('book-list', views.book_list, name="book-list"),
    # path('clear-cookie', views.clear_cookie, name='clear-cookies'),
    path('book/<book_id>', views.book_methods, name='book-methods'),
    path('book/<book_id>/rent', views.rent_book, name='book-rent'),
    path('rents-list', views.rent_list, name='rents-list')
]