from django.urls import path
from .views import UserView, ChannelView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('topic/', ChannelView.as_view()),
]