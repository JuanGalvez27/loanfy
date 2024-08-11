from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
import uuid

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    id_number = models.CharField(help_text="ID Number", null=True, blank=True, max_length=255)

