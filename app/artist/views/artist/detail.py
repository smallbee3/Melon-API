import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from ...models import Artist

__all__ = (
    'artist_detail',
)


def artist_detail(request, artist_pk):
    # artist_pk에 해당하는 Artist정보 보여주기
    # Template: artist/artist_detail.html
    # URL: /3/
    artist = get_object_or_404(Artist, pk=artist_pk)

    # YouTube에서 아티스트명으로 검색한 결과 가져오기
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': '10',
        'q': artist.name,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    context = {
        'artist': artist,
        # YouTube검색 후 전달받은 데이터의 'items'값
        'youtube_items': response_dict['items'],
    }
    return render(request, 'artist/artist_detail.html', context)
