from django.urls import path, include
from . import views

urlpatterns = [
    path('all_videos/', views.Videos.as_view()),
    path('video/', views.Video.as_view()),
    path('ask_question/', views.QuestionAnswering.as_view()),
    path('upload/', views.FileUpload.as_view()),
    path('youtube_video/', views.YoutubeDownloader.as_view()),
]