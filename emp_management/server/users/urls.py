from django.urls import path
from .views import LoginView, LogoutView, RegisterUserAPIView
# from rest_framework.authtoken import views

urlpatterns = [
    # path("get-details", UserDetailAPI.as_view()),
    path("register", RegisterUserAPIView.as_view()),
    # path("api-token-auth", views.obtain_auth_token),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
