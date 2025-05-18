from django.shortcuts import render


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import FavoriteRepo, UserProfile

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FavoriteRepo

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

def add_to_favorites(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            FavoriteRepo.objects.get_or_create(
                user=request.user,
                repo_name=data['full_name'],
                repo_url=data['html_url'],
                defaults={
                    'description': data.get('description', ''),
                    'language': data.get('language', ''),
                    'stars': int(data.get('stars', 0)),
                }
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

# views.py
@login_required
def delete_favorite(request, repo_id):
    FavoriteRepo.objects.filter(id=repo_id, user=request.user).delete()
    return redirect('user_dashboard')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import FavoriteRepo

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import FavoriteRepo

@login_required
def profile_view(request):
    user = request.user
    favorite_repos = FavoriteRepo.objects.filter(user=user)
    user_repos = []
    github_username = None

    # Ensure UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        github_username = request.POST.get('github_username', '').strip()
        if github_username:
            profile.github_username = github_username
            profile.save()

    try:
        github_username = profile.github_username
    except Exception:
        github_username = None

    if github_username:
        url = f"https://api.github.com/users/{github_username}/repos"
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_repos = response.json()
        else:
            user_repos = []

    context = {
        'username': user.username,
        'favorite_repos': favorite_repos,
        'user_repos': user_repos,
    }
    return render(request, 'user_profile_app/profile.html', context)
