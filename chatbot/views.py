from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.files_processing import load_dict_from_json
from chatbot.serializers import ChatRequestSerializer, ChatMessageSerializer
from chatbot.models import ChatSession, ChatMessage
from utils.chat import qa_chat_with_prompt
from logging_config import get_logger
import json
import uuid
from config import *

logger = get_logger(__name__)

# Create your views here.
class ChatbotAPIView(APIView):
    """API View for chat"""
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data = request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            query = serializer.validated_data['query']
            llm_name = serializer.validated_data["llm_name"]
            session_id = serializer.validated_data.get('session_id')

            if not session_id:
                session_id = str(uuid.uuid4())

            session, _ = ChatSession.objects.get_or_create(id = session_id)

            chat_history = list(session.chatmessages.all()
                                .order_by("timestamp")
                                .values("role", "message"))

            try:
                response = qa_chat_with_prompt(text = text,
                                           query = query,
                                           chat_history = chat_history,
                                            llm_name = llm_name)
                full_response = f"Answer: {response["answer"]}\nSource: {response['source']}"

                ChatMessage.objects.create(session=session,
                                           role="user",
                                           message=query)

                ChatMessage.objects.create(session = session,
                                           role = "assistant",
                                           message = full_response)

                chat_history = ChatMessageSerializer(session.chatmessages.all(), many=True).data

                return Response({ "session_id": str(session.id),
                                  "query":query,
                                  "response": full_response,
                                 "chat_history": chat_history},
                                status = status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Chatbot API error: {str(e)}")
                return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# Create your views here.
