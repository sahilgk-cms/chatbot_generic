from chatbot.views import ChatbotAPIView
from django.urls import path

urlpatterns = [
    path("chat/", ChatbotAPIView.as_view(), name = "chat")
]