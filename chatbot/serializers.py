from rest_framework import serializers
from .models import ChatMessage

class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat request"""
    text = serializers.CharField()
    query = serializers.CharField()
    llm_name = serializers.CharField()
    session_id = serializers.CharField(required = False, allow_blank = True)


class ChatMessageSerializer(serializers.ModelSerializer):
    """Model Serializer for chat message"""
    class Meta:
        model = ChatMessage
        fields = ["role", "message", "timestamp"]