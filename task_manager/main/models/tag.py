import uuid
from django.db import models
from .base_model import BaseModel


class Tag(BaseModel):
    title = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
