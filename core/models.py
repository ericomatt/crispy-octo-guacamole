from django.db import models


class FeatureRequest(models.Model):
    """Model representing a feature request."""

    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    vote_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-vote_count', '-created_at']

    def __str__(self):
        return str(self.title)
