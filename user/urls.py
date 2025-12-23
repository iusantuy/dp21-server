from django.urls import path
from user.presentation.views import LoginView, LogoutView, MeView, get_csrf

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("csrf/", get_csrf, name="get-csrf")
]










# # users/urls.py
# from django.urls import path
# from .presentation.views import RegisterView, LoginView
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     path("register/", RegisterView.as_view(), name="register"),
#     path("login/", LoginView.as_view(), name="login"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]
