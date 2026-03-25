from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from .models import FeatureRequest, Vote


def feature_request_list(request):
    """Display list of all feature requests sorted by vote count.

    REQ-002: Sorted by vote count descending (highest votes first).
    Uses annotation to compute vote_count for proper database sorting.
    """
    # REQ-004: Rank by vote count - annotate with vote count and order by it
    # Use 'votes_count' (plural) to avoid conflict with the property
    feature_requests = (
        FeatureRequest.objects
        .annotate(votes_count=Count('votes'))
        .order_by('-votes_count', '-created_at')
    )

    # Get session key for tracking user's votes
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Get IDs of feature requests the user has voted for
    voted_ids = list(
        Vote.objects
        .filter(session_key=session_key)
        .values_list('feature_request_id', flat=True)
    )

    context = {
        'feature_requests': feature_requests,
        'voted_ids': voted_ids,
    }
    return render(request, 'core/feature_request_list.html', context)


@require_POST
def create_feature_request(request):
    """Create a new feature request."""
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()

    # REQ-001: Validation - title and description required
    if not title:
        messages.error(request, 'Title is required.')
        return redirect('feature_request_list')

    if not description:
        messages.error(request, 'Description is required.')
        return redirect('feature_request_list')

    FeatureRequest.objects.create(title=title, description=description)
    messages.success(request, 'Feature request submitted successfully!')
    return redirect('feature_request_list')


@require_POST
def toggle_vote(request, pk):
    """Toggle vote on a feature request.

    REQ-003: Upvote functionality with toggle behavior.
    Uses session to track user's votes for duplicate prevention.
    """
    feature_request = get_object_or_404(FeatureRequest, pk=pk)

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Check if user has already voted
    existing_vote = Vote.objects.filter(
        feature_request=feature_request,
        session_key=session_key
    ).first()

    if existing_vote:
        # Toggle off: remove the vote
        existing_vote.delete()
    else:
        # Toggle on: create new vote
        Vote.objects.create(
            feature_request=feature_request,
            session_key=session_key
        )

    return redirect('feature_request_list')


@require_POST
def api_toggle_vote(request, pk):
    """AJAX endpoint for voting - provides immediate UI updates.

    REQ-003: Performance requirement - UI updates immediately.
    Returns JSON response for client-side UI update without page reload.
    """
    feature_request = get_object_or_404(FeatureRequest, pk=pk)

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Check if user has already voted
    existing_vote = Vote.objects.filter(
        feature_request=feature_request,
        session_key=session_key
    ).first()

    if existing_vote:
        # Toggle off: remove the vote
        existing_vote.delete()
        has_voted = False
    else:
        # Toggle on: create new vote
        Vote.objects.create(
            feature_request=feature_request,
            session_key=session_key
        )
        has_voted = True

    # Get updated vote count
    vote_count = feature_request.vote_count

    return JsonResponse({
        'success': True,
        'vote_count': vote_count,
        'has_voted': has_voted,
    })
