from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class ChatSession(models.Model):
    """For creating and storing sessions"""
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Session: {self.id}"


class ChatMessage(models.Model):
    """For creating and storing chat messages within a session"""
    id = models.BigAutoField(primary_key = True)
    role = models.CharField(max_length = 20, choices = [("user", "User"), ("assistant", "Assistant")])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(ChatSession, on_delete = models.CASCADE, related_name = "chatmessages")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.role}: {self.message[:50]}"


