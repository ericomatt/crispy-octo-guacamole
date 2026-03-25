from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import FeatureRequest


def feature_request_list(request):
    """Display list of all feature requests sorted by vote count."""
    feature_requests = FeatureRequest.objects.all()

    voted_ids = request.session.get('voted_requests', [])

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

    if not title or not description:
        messages.error(request, 'Title and description are required.')
        return redirect('feature_request_list')

    FeatureRequest.objects.create(title=title, description=description)
    messages.success(request, 'Feature request submitted successfully!')
    return redirect('feature_request_list')


@require_POST
def toggle_vote(request, pk):
    """Toggle vote on a feature request."""
    feature_request = get_object_or_404(FeatureRequest, pk=pk)

    voted_requests = request.session.get('voted_requests', [])

    if pk in voted_requests:
        voted_requests.remove(pk)
        feature_request.vote_count = max(0, feature_request.vote_count - 1)
    else:
        voted_requests.append(pk)
        feature_request.vote_count += 1

    feature_request.save()
    request.session['voted_requests'] = voted_requests

    return redirect('feature_request_list')
