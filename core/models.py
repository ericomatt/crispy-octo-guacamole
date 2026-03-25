from django.db import models


class FeatureRequest(models.Model):
    """Model representing a feature request."""

    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def vote_count(self):
        """Return the total number of votes for this feature request.
        
        Note: For database queries, use annotate(vote_count=Count('votes')) instead.
        """
        return self.votes.count()


class Vote(models.Model):
    """Model to track votes on feature requests.
    
    Uses session_key to identify anonymous users, ensuring data integrity
    and preventing duplicate votes from the same browser session.
    """

    feature_request = models.ForeignKey(
        FeatureRequest,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    session_key = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure one vote per session per feature request
        unique_together = ['feature_request', 'session_key']
        indexes = [
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"Vote by {self.session_key} on {self.feature_request.title}"
