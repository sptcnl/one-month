from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=150)

    def __str__(self):
        return self.username


class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')