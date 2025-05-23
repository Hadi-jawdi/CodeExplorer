from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import FavoriteRepo

def home(request):
    return render(request, 'core/home.html')

@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        repo_name = request.POST.get('repo_name')
        repo_url = request.POST.get('repo_url')
        description = request.POST.get('description')
        language = request.POST.get('language')
        stars = request.POST.get('stars')

        # Check if this specific user already has this repo in favorites
        existing_favorite = FavoriteRepo.objects.filter(
            user=request.user,
            repo_url=repo_url
        ).first()

        if existing_favorite:
            messages.warning(request, 'This repository is already in your favorites!')
        else:
            # Create new favorite
            FavoriteRepo.objects.create(
                user=request.user,
                repo_name=repo_name,
                repo_url=repo_url,
                description=description,
                language=language,
                stars=stars
            )
            profile_url = reverse('user_profile_app:profile')
            profile_link = f'<a href="{profile_url}" class="alert-link">View in Profile</a>'
            messages.success(request, mark_safe(f'Repository added to favorites! {profile_link}'))

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def search_projects(request):
    query = request.GET.get('q', '')
    language = request.GET.get('language', '')
    
    if not query:
        return render(request, 'core/home.html', {
            'error_message': 'Please enter a search query',
            'query': query,
            'language': language
        })

    # Build the search query
    search_query = query
    if language:
        search_query += f" language:{language}"

    url = "https://api.github.com/search/repositories"
    params = {
        'q': search_query,
        'sort': 'stars',
        'order': 'desc'
    }
    
    headers = {}
    if hasattr(settings, 'GITHUB_TOKEN') and settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        repos = data.get('items', [])
        
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(repos, 6)  # Show 6 repos per page
        
        try:
            repos_page = paginator.page(page)
        except PageNotAnInteger:
            repos_page = paginator.page(1)
        except EmptyPage:
            repos_page = paginator.page(paginator.num_pages)

        return render(request, 'core/home.html', {
            'repos': repos_page,
            'query': query,
            'language': language,
            'paginator': paginator,
            'page_obj': repos_page,
        })
        
    except requests.exceptions.RequestException as e:
        error_message = "Error connecting to GitHub API. Please try again later."
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 403:
                error_message = "GitHub API rate limit exceeded. Please try again later."
            elif e.response.status_code == 401:
                error_message = "GitHub API authentication failed. Please check your token."
        
        return render(request, 'core/home.html', {
            'error_message': error_message,
            'query': query,
            'language': language
        })
