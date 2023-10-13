from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Descriptions.as_view()),
    path('star/', views.Star.as_view())
]