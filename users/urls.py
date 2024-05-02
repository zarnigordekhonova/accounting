from django.urls import path

from users.views import RegisterAPIView, password_change_view

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('password_change/', password_change_view, name="password_change"),
]
