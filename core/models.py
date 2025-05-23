from django.db import models
from django.contrib.auth.models import User

class FavoriteRepo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=255)
    repo_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'repo_url')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.repo_name}"
