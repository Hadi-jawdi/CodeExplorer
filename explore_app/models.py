from django.db import models
from django.contrib.auth.models import User

class FavoriteRepo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_repos')
    repo_id = models.PositiveIntegerField()
    repo_name = models.CharField(max_length=255)
    repo_url = models.URLField()
    repo_description = models.TextField(blank=True, null=True)
    repo_language = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'repo_id')

    def __str__(self):
        return f"{self.repo_name} favorited by {self.user.username}"
