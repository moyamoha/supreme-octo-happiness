from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("signin/", views.MyTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", views.SignupApi.as_view(), name="signup"),
    path("changePassword", views.ChangePassword.as_view(), name="change_password"),
    path("todos", views.AllTodos.as_view()),
    path("todos/<int:pk>", views.TodoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns=urlpatterns)
