from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.sign_up, name="sign_up"),
    path('borrow/<str:slug>', views.borrow, name='borrow'),
    path('book/<str:slug>', views.book_details, name='book'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<str:slug>', views.edit_book, name='edit_book'),
    path('delete_book/<str:slug>', views.delete_book, name='delete_book'),
    path('request_book/', views.request_book, name='request_book'),
    path('history/', views.history, name='history'),
]