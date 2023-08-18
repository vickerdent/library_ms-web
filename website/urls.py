from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('signup/', views.sign_up, name="sign_up"),
    path('borrow/<str:book>', views.borrow, name='borrow'),
    path('book/<str:book>', views.book_details, name='book'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_book/<str:dname>/<str:dauthor>', views.add_book, name='add_a_book'),
    path('edit_book/<str:book>', views.edit_book, name='edit_book'),
    path('edit_book_image/<str:book>', views.edit_book_image, name='edit_book_image'),
    path('delete_book/<str:book>', views.delete_book, name='delete_book'),
    path('request_book/', views.request_book, name='request_book'),
    path('history/', views.history, name='history'),
    path('return_book/', views.return_book, name='return_book'),
    path('process_return/<str:book>', views.process_return, name='process_return'),
    path('requested_books/', views.requested_books, name='requested_books'),
    path('delete_request/<str:dname>/<str:dauthor>', views.delete_request, name='delete_request'),
    path('confirm_code/', views.confirm_code, name='confirm_code'),
    path('resend_code/', views.resend_code, name='resend_code'),
]