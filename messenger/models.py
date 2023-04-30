from uuid import uuid4
from django.db import models

from core.models import BaseModel
from account.models import User


class Chat(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name="chats")

    def __str__(self) -> str:
        return self.title


class Message(BaseModel):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")

    def __str__(self) -> str:
        return self.content
