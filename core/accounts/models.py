import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    class Meta:
        verbose_name_plural = '프로필'
        db_table = 'Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
