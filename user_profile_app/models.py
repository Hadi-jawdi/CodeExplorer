from django.db import models


# models.py
from django.db import models
from django.contrib.auth.models import User

class FavoriteRepo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    repo_name = models.CharField(max_length=255)
    repo_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    stars = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repo_name} ({self.user.username})"
