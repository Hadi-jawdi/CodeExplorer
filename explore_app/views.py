import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import FavoriteRepo
import requests

def explore(request):
    """
    View to fetch great and famous repositories from GitHub API and render them.
    """
    url = "https://api.github.com/search/repositories"
    base_query = "stars:>50000"
    language_filter = request.GET.get("language", "").strip()
    category_filter = request.GET.get("category", "").strip()

    # Build the query string for GitHub API
    query_parts = [base_query]
    if category_filter and category_filter.lower() != "all":
        # Map category to GitHub topics or keywords
        category_map = {
            "ai_ml": "topic:machine-learning",
            "web_dev": "topic:web-development",
            "mobile_apps": "topic:mobile",
        }
        category_query = category_map.get(category_filter.lower(), "")
        if category_query:
            query_parts.append(category_query)
    if language_filter and language_filter.lower() != "all":
        query_parts.append(f"language:{language_filter}")

    full_query = " ".join(query_parts)

    params = {
        "q": full_query,
        "sort": "stars",
        "order": "desc",
        "per_page": 9
    }
    headers = {}
    token = getattr(settings, "GITHUB_TOKEN", None)
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(url, params=params, headers=headers)
    repos = []
    if response.status_code == 200:
        data = response.json()
        repos = data.get("items", [])
    else:
        # fallback empty list or handle error as needed
        repos = []

    context = {
        "repositories": repos,
        "language_filter": language_filter,
        "category_filter": category_filter,
    }
    return render(request, "explore_app/explore.html", context)

@login_required
@require_POST
def add_favorite(request):
    """
    View to add a repository to user's favorites.
    """
    user = request.user
    repo_id = request.POST.get("repo_id")
    repo_name = request.POST.get("repo_name")
    repo_url = request.POST.get("repo_url")
    repo_description = request.POST.get("repo_description", "")
    repo_language = request.POST.get("repo_language", "")

    if repo_id and repo_name and repo_url:
        # Check if already favorited
        favorite, created = FavoriteRepo.objects.get_or_create(
            user=user,
            repo_id=repo_id,
            defaults={
                "repo_name": repo_name,
                "repo_url": repo_url,
                "repo_description": repo_description,
                "repo_language": repo_language,
            }
        )
    return redirect("explore_app:explore")
