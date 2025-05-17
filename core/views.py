from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

import requests
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_projects(request):
    query = request.GET.get('q', 'django')
    language = request.GET.get('language')

    url = f"https://api.github.com/search/repositories?q={query}+in:name"
    if language:
        url += f"+language:{language}"

    headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    repos = data.get('items', [])

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(repos, 5)  # Show 5 repos per page
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
