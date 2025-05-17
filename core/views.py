from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

import requests
from django.conf import settings
from django.shortcuts import render

def search_projects(request):
    query = request.GET.get('q', 'django')
    language = request.GET.get('language')

    url = f"https://api.github.com/search/repositories?q={query}+in:name"
    if language:
        url += f"+language:{language}"

    headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    return render(request, 'core/home.html', {
        'repos': data.get('items', []),
        'query': query,
        'language': language,
    })
