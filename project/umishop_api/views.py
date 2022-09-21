from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .tasks import send_email, send_slack_msg


# Create your views here.


class UserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChannelView(APIView):

    def post(self, request):
        user_email = request.data.get('email')
        question = request.data.get('question')
        username = request.data.get('username')
        topic = request.data.get('topic')

        if topic == 'sales':
            send_email(question, username, user_email, settings.EMAIL_SALES)
            Response(status=status.HTTP_200_OK)
        elif topic == 'pricing':
            send_slack_msg(question, settings.SLACK_CHANNEL)
            Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
