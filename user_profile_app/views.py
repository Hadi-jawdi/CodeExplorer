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

from django.contrib import messages
import requests
from django.conf import settings

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        bio = request.POST.get('bio', '').strip()
        profile_photo = request.FILES.get('profile_photo')
        
        if bio:
            profile.bio = bio
        if profile_photo:
            profile.profile_photo = profile_photo
            
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile_app:profile')
    
    return redirect('user_profile_app:profile')

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
    return redirect('user_profile_app:profile')


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
    github_profile_data = None
    error_message = None

    # Ensure UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Check if user logged in with GitHub
    social_auth = user.social_auth.filter(provider='github').first()
    
    if social_auth:
        # User logged in with GitHub, get their username
        github_username = social_auth.extra_data.get('login')
        if github_username:
            profile.github_username = github_username
            profile.save()
    elif request.method == 'POST':
        # Manual GitHub username entry
        github_username_input = request.POST.get('github_username', '').strip()
        if github_username_input:
            # Validate GitHub username existence
            url_user = f"https://api.github.com/users/{github_username_input}"
            headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
            response_user = requests.get(url_user, headers=headers)
            if response_user.status_code == 200:
                profile.github_username = github_username_input
                profile.save()
                github_username = github_username_input
                github_profile_data = response_user.json()
                error_message = None
            else:
                github_username = None
                error_message = "The entered username is not a valid GitHub username."
        else:
            github_username = None
            error_message = None
    else:
        # Try to get existing GitHub username from profile
        try:
            github_username = profile.github_username
        except Exception:
            github_username = None

    # Fetch GitHub profile data if we have a username
    if github_username:
        url_user = f"https://api.github.com/users/{github_username}"
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        response_user = requests.get(url_user, headers=headers)
        if response_user.status_code == 200:
            github_profile_data = response_user.json()
            
            # Fetch repositories
            url = f"https://api.github.com/users/{github_username}/repos"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_repos = response.json()
                # Sort repos by stars and last updated
                user_repos.sort(key=lambda x: (x.get('stargazers_count', 0), x.get('updated_at', '')), reverse=True)
            else:
                user_repos = []

    context = {
        'username': user.username,
        'favorite_repos': favorite_repos,
        'user_repos': user_repos,
        'github_username': github_username,
        'github_profile_data': github_profile_data,
        'error_message': error_message,
        'profile': profile,
        'is_github_connected': bool(social_auth),
    }
    return render(request, 'user_profile_app/profile.html', context)
