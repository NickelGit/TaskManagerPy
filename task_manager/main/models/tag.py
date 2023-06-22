from django.db import models
from .base_model import BaseModel


class Tag(BaseModel):
    title = models.CharField(max_length=50)
