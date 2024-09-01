from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID field as primary key
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Custom related name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Keep 'username' as required, but use 'email' for authentication

    def save(self, *args, **kwargs):
        # Convert email to lowercase for case-insensitive login
        self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)

class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID field as primary key
    sender = models.ForeignKey(CustomUser, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID field as primary key
    user = models.ForeignKey(CustomUser, related_name="friendships", on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name="friends", on_delete=models.CASCADE)
