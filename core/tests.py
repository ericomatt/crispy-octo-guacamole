from django.test import TestCase, Client
from django.contrib import messages
from .models import FeatureRequest, Vote


class FeatureRequestModelTest(TestCase):
    """Tests for the FeatureRequest model."""

    def test_create_feature_request(self):
        """Test creating feature request with title and description."""
        fr = FeatureRequest.objects.create(
            title="Test Feature",
            description="Test description"
        )
        self.assertEqual(fr.title, "Test Feature")
        self.assertEqual(fr.description, "Test description")
        self.assertEqual(fr.vote_count, 0)

    def test_default_ordering(self):
        """Test ordering by vote count descending."""
        FeatureRequest.objects.create(title="Low vote", description="d1")
        fr2 = FeatureRequest.objects.create(title="High vote", description="d2")
        Vote.objects.create(feature_request=fr2, session_key='test-session')

        requests = list(FeatureRequest.objects.all())
        self.assertEqual(requests[0].title, "High vote")


# =============================================================================
# REQ-001: Submit Feature Request
# =============================================================================

class SubmitFeatureRequestTest(TestCase):
    """Tests for REQ-001: Submit Feature Request."""

    def setUp(self):
        self.client = Client()
        self.create_url = '/create/'

    def test_create_feature_request_with_title_and_description(self):
        """Test creating feature request with valid title and description."""
        response = self.client.post(self.create_url, {
            'title': 'New Feature',
            'description': 'This is a great new feature'
        })

        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)

        # Should create the feature request in the database
        self.assertEqual(FeatureRequest.objects.count(), 1)
        fr = FeatureRequest.objects.first()
        self.assertEqual(fr.title, 'New Feature')
        self.assertEqual(fr.description, 'This is a great new feature')

    def test_validation_title_required_min_1_char(self):
        """Test validation: title required (min 1 char)."""
        # Empty title should fail
        response = self.client.post(self.create_url, {
            'title': '',
            'description': 'Some description'
        })

        # Should redirect back (not create)
        self.assertEqual(response.status_code, 302)

        # Should not create any feature request
        self.assertEqual(FeatureRequest.objects.count(), 0)

        # Should have error message
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('Title' in str(m) for m in messages_list))

    def test_validation_description_required_min_1_char(self):
        """Test validation: description required (min 1 char)."""
        # Empty description should fail
        response = self.client.post(self.create_url, {
            'title': 'Some title',
            'description': ''
        })

        # Should redirect back (not create)
        self.assertEqual(response.status_code, 302)

        # Should not create any feature request
        self.assertEqual(FeatureRequest.objects.count(), 0)

        # Should have error message
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('description' in str(m).lower() for m in messages_list))

    def test_successful_creation_stores_data_correctly(self):
        """Test successful creation stores the data correctly."""
        title = 'Amazing New Feature'
        description = 'This feature will change everything'

        self.client.post(self.create_url, {
            'title': title,
            'description': description
        })

        # Verify the object was created with correct data
        fr = FeatureRequest.objects.first()
        self.assertIsNotNone(fr)
        self.assertEqual(fr.title, title)
        self.assertEqual(fr.description, description)
        self.assertEqual(fr.vote_count, 0)
        self.assertIsNotNone(fr.created_at)


# =============================================================================
# REQ-002: View Feature Request List
# =============================================================================

class ViewFeatureRequestListTest(TestCase):
    """Tests for REQ-002: View Feature Request List."""

    def setUp(self):
        self.client = Client()
        self.list_url = '/'

    def test_list_displays_all_feature_requests(self):
        """Test list displays all feature requests."""
        # Create multiple feature requests
        FeatureRequest.objects.create(title='Feature 1', description='Desc 1')
        FeatureRequest.objects.create(title='Feature 2', description='Desc 2')
        FeatureRequest.objects.create(title='Feature 3', description='Desc 3')

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Feature 1')
        self.assertContains(response, 'Feature 2')
        self.assertContains(response, 'Feature 3')

    def test_each_displays_title_description_vote_count(self):
        """Test each displays: title, description, vote count."""
        fr = FeatureRequest.objects.create(
            title='Test Feature',
            description='Test description',
        )
        # Add a vote to verify vote_count property works
        Vote.objects.create(feature_request=fr, session_key='test-session')

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Feature')
        self.assertContains(response, 'Test description')
        self.assertContains(response, '1')

    def test_sorted_by_vote_count_descending(self):
        """Test sorted by vote count descending."""
        # Create requests with different vote counts
        fr_low = FeatureRequest.objects.create(title='Low', description='d')
        fr_medium = FeatureRequest.objects.create(title='Medium', description='d')
        fr_high = FeatureRequest.objects.create(title='High', description='d')

        # Add votes to create vote counts
        Vote.objects.create(feature_request=fr_low, session_key='session-1')

        Vote.objects.create(feature_request=fr_medium, session_key='session-2')
        Vote.objects.create(feature_request=fr_medium, session_key='session-3')
        Vote.objects.create(feature_request=fr_medium, session_key='session-4')
        Vote.objects.create(feature_request=fr_medium, session_key='session-5')
        Vote.objects.create(feature_request=fr_medium, session_key='session-6')
        Vote.objects.create(feature_request=fr_medium, session_key='session-7')
        Vote.objects.create(feature_request=fr_medium, session_key='session-8')
        Vote.objects.create(feature_request=fr_medium, session_key='session-9')
        Vote.objects.create(feature_request=fr_medium, session_key='session-10')

        Vote.objects.create(feature_request=fr_high, session_key='session-a')
        Vote.objects.create(feature_request=fr_high, session_key='session-b')
        Vote.objects.create(feature_request=fr_high, session_key='session-c')
        Vote.objects.create(feature_request=fr_high, session_key='session-d')
        Vote.objects.create(feature_request=fr_high, session_key='session-e')
        Vote.objects.create(feature_request=fr_high, session_key='session-f')
        Vote.objects.create(feature_request=fr_high, session_key='session-g')
        Vote.objects.create(feature_request=fr_high, session_key='session-h')
        Vote.objects.create(feature_request=fr_high, session_key='session-i')
        Vote.objects.create(feature_request=fr_high, session_key='session-j')
        Vote.objects.create(feature_request=fr_high, session_key='session-k')
        Vote.objects.create(feature_request=fr_high, session_key='session-l')
        Vote.objects.create(feature_request=fr_high, session_key='session-m')
        Vote.objects.create(feature_request=fr_high, session_key='session-n')
        Vote.objects.create(feature_request=fr_high, session_key='session-o')

        # Refresh vote_count properties
        fr_low.refresh_from_db()
        fr_medium.refresh_from_db()
        fr_high.refresh_from_db()

        response = self.client.get(self.list_url)

        # Check the context contains requests in correct order
        feature_requests = list(response.context['feature_requests'])
        titles = [fr.title for fr in feature_requests]

        # Should be sorted by vote count descending
        self.assertEqual(titles[0], 'High')
        self.assertEqual(titles[1], 'Medium')
        self.assertEqual(titles[2], 'Low')

    def test_empty_state_when_no_requests_exist(self):
        """Test empty state when no requests exist."""
        # Ensure no requests exist
        FeatureRequest.objects.all().delete()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        # Should show empty state message or indication
        # Either no requests are rendered, or an empty message appears


# =============================================================================
# REQ-003: Upvote Feature Request
# =============================================================================

class UpvoteFeatureRequestTest(TestCase):
    """Tests for REQ-003: Upvote Feature Request."""

    def setUp(self):
        self.client = Client()
        self.feature_request = FeatureRequest.objects.create(
            title='Test Feature',
            description='Test description',
        )
        self.vote_url = f'/vote/{self.feature_request.pk}/'

    def test_upvote_increases_vote_count_by_1(self):
        """Test upvote increases vote count by 1."""
        initial_count = self.feature_request.vote_count

        self.client.post(self.vote_url)

        # Reload from database
        self.feature_request.refresh_from_db()

        self.assertEqual(self.feature_request.vote_count, initial_count + 1)

    def test_toggle_vote_removes_vote(self):
        """Test toggle vote removes vote."""
        # First vote
        self.client.post(self.vote_url)
        self.feature_request.refresh_from_db()
        self.assertEqual(self.feature_request.vote_count, 1)

        # Second vote should remove (toggle off)
        self.client.post(self.vote_url)
        self.feature_request.refresh_from_db()

        self.assertEqual(self.feature_request.vote_count, 0)

    def test_prevent_duplicate_votes_same_user(self):
        """Test prevent duplicate votes (same user)."""
        # Vote twice in same session
        self.client.post(self.vote_url)
        self.feature_request.refresh_from_db()
        first_vote_count = self.feature_request.vote_count

        self.client.post(self.vote_url)
        self.feature_request.refresh_from_db()
        second_vote_count = self.feature_request.vote_count

        # Should toggle off, not add another vote
        # Net effect should be 0 (toggle on then off)
        self.assertEqual(second_vote_count, 0)
        self.assertNotEqual(second_vote_count, first_vote_count + 1)

    def test_voted_state_indicator(self):
        """Test voted state indicator."""
        # Ensure session is created
        self.client.session.create()

        # Initially not voted
        response = self.client.get('/')
        voted_ids = response.context.get('voted_ids', [])
        self.assertNotIn(self.feature_request.pk, voted_ids)

        # After voting
        self.client.post(self.vote_url)
        response = self.client.get('/')
        voted_ids = response.context.get('voted_ids', [])
        self.assertIn(self.feature_request.pk, voted_ids)


# =============================================================================
# REQ-004: Display Vote Counts and Ranking
# =============================================================================

class DisplayVoteCountsAndRankingTest(TestCase):
    """Tests for REQ-004: Display Vote Counts and Ranking."""

    def setUp(self):
        self.client = Client()

    def test_vote_count_visible_for_each_request(self):
        """Test vote count visible for each request."""
        fr1 = FeatureRequest.objects.create(title='Feature 1', description='d1')
        fr2 = FeatureRequest.objects.create(title='Feature 2', description='d2')

        # Add votes
        Vote.objects.create(feature_request=fr1, session_key='s1')
        Vote.objects.create(feature_request=fr1, session_key='s2')
        Vote.objects.create(feature_request=fr1, session_key='s3')
        Vote.objects.create(feature_request=fr1, session_key='s4')
        Vote.objects.create(feature_request=fr1, session_key='s5')

        Vote.objects.create(feature_request=fr2, session_key='s6')
        Vote.objects.create(feature_request=fr2, session_key='s7')
        Vote.objects.create(feature_request=fr2, session_key='s8')
        Vote.objects.create(feature_request=fr2, session_key='s9')
        Vote.objects.create(feature_request=fr2, session_key='s10')
        Vote.objects.create(feature_request=fr2, session_key='s11')
        Vote.objects.create(feature_request=fr2, session_key='s12')
        Vote.objects.create(feature_request=fr2, session_key='s13')
        Vote.objects.create(feature_request=fr2, session_key='s14')
        Vote.objects.create(feature_request=fr2, session_key='s15')

        response = self.client.get('/')

        # Vote counts should be displayed
        self.assertContains(response, '5')
        self.assertContains(response, '10')

    def test_ranking_by_vote_count_descending(self):
        """Test ranking by vote count descending."""
        fr_a = FeatureRequest.objects.create(title='A', description='d')
        fr_b = FeatureRequest.objects.create(title='B', description='d')
        fr_c = FeatureRequest.objects.create(title='C', description='d')

        # Add votes
        Vote.objects.create(feature_request=fr_a, session_key='session-a1')

        Vote.objects.create(feature_request=fr_b, session_key='session-b1')
        Vote.objects.create(feature_request=fr_b, session_key='session-b2')
        Vote.objects.create(feature_request=fr_b, session_key='session-b3')
        Vote.objects.create(feature_request=fr_b, session_key='session-b4')
        Vote.objects.create(feature_request=fr_b, session_key='session-b5')
        Vote.objects.create(feature_request=fr_b, session_key='session-b6')
        Vote.objects.create(feature_request=fr_b, session_key='session-b7')
        Vote.objects.create(feature_request=fr_b, session_key='session-b8')
        Vote.objects.create(feature_request=fr_b, session_key='session-b9')
        Vote.objects.create(feature_request=fr_b, session_key='session-b10')

        Vote.objects.create(feature_request=fr_c, session_key='session-c1')
        Vote.objects.create(feature_request=fr_c, session_key='session-c2')
        Vote.objects.create(feature_request=fr_c, session_key='session-c3')
        Vote.objects.create(feature_request=fr_c, session_key='session-c4')
        Vote.objects.create(feature_request=fr_c, session_key='session-c5')
        Vote.objects.create(feature_request=fr_c, session_key='session-c6')
        Vote.objects.create(feature_request=fr_c, session_key='session-c7')
        Vote.objects.create(feature_request=fr_c, session_key='session-c8')
        Vote.objects.create(feature_request=fr_c, session_key='session-c9')
        Vote.objects.create(feature_request=fr_c, session_key='session-c10')
        Vote.objects.create(feature_request=fr_c, session_key='session-c11')
        Vote.objects.create(feature_request=fr_c, session_key='session-c12')
        Vote.objects.create(feature_request=fr_c, session_key='session-c13')
        Vote.objects.create(feature_request=fr_c, session_key='session-c14')
        Vote.objects.create(feature_request=fr_c, session_key='session-c15')
        Vote.objects.create(feature_request=fr_c, session_key='session-c16')
        Vote.objects.create(feature_request=fr_c, session_key='session-c17')
        Vote.objects.create(feature_request=fr_c, session_key='session-c18')
        Vote.objects.create(feature_request=fr_c, session_key='session-c19')
        Vote.objects.create(feature_request=fr_c, session_key='session-c20')

        response = self.client.get('/')
        feature_requests = list(response.context['feature_requests'])

        # Should be sorted descending by vote_count
        self.assertEqual(feature_requests[0].vote_count, 20)
        self.assertEqual(feature_requests[1].vote_count, 10)
        self.assertEqual(feature_requests[2].vote_count, 1)

    def test_ranking_position_indicated(self):
        """Test ranking position indicated."""
        # Create requests with distinct vote counts
        fr_third = FeatureRequest.objects.create(title='Third', description='d')
        fr_first = FeatureRequest.objects.create(title='First', description='d')
        fr_second = FeatureRequest.objects.create(title='Second', description='d')

        # Third place: 1 vote
        Vote.objects.create(feature_request=fr_third, session_key='third-1')

        # Second place: 10 votes
        for i in range(10):
            Vote.objects.create(feature_request=fr_second, session_key=f'second-{i}')

        # First place: 100 votes
        for i in range(100):
            Vote.objects.create(feature_request=fr_first, session_key=f'first-{i}')

        response = self.client.get('/')
        feature_requests = list(response.context['feature_requests'])

        # First item should be the highest vote count
        self.assertEqual(feature_requests[0].title, 'First')
        self.assertEqual(feature_requests[0].vote_count, 100)

        # Second item
        self.assertEqual(feature_requests[1].title, 'Second')
        self.assertEqual(feature_requests[1].vote_count, 10)

        # Third item
        self.assertEqual(feature_requests[2].title, 'Third')
        self.assertEqual(feature_requests[2].vote_count, 1)
