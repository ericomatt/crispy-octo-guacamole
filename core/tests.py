from django.test import TestCase
from django.contrib import messages
from .models import FeatureRequest


class FeatureRequestModelTest(TestCase):
    def test_create_feature_request(self):
        fr = FeatureRequest.objects.create(
            title="Test Feature",
            description="Test description"
        )
        self.assertEqual(fr.title, "Test Feature")
        self.assertEqual(fr.vote_count, 0)

    def test_default_ordering(self):
        FeatureRequest.objects.create(title="Low vote", description="d1")
        fr2 = FeatureRequest.objects.create(title="High vote", description="d2")
        fr2.vote_count = 10
        fr2.save()
        requests = list(FeatureRequest.objects.all())
        self.assertEqual(requests[0].title, "High vote")
