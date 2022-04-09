from django.urls import path, include
from .views import *


urlpatterns = [
    path('video_feed', video_feed, name='video_feed'),
    path('teacher', teacherView, name='teacher'),
    path('testt', testt, name='testt'),
    path('', loginView, name='login'),
    path('verify', verifyView, name="verify"),
    path('student', studentView, name='student'),
    path('teacher', teacherView, name='teacher'),
    path('logout', logoutUser, name="logout"),
    path('actionUrl', RecordTrain),
    path('testUrl', RecordTest),
    path('exam', examView, name='exam'),
    ]
