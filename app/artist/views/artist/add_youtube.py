from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from artist.models import Artist

__all__ = (
    'artist_add_youtube',
)


def artist_add_youtube(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    # artist_pk에 해당하는 Artist에게
    # request.POST로 전달된 youtube_id, title, url_thumbnail을 가지는
    #   ArtistYouTube를 Artist의 youtube_videos에 추가
    artist.youtube_videos.update_or_create(
        youtube_id=request.POST['youtube_id'],
        defaults={
            'title': request.POST['title'],
            'url_thumbnail': request.POST['url_thumbnail'],
        }
    )
    next_path = request.POST.get(
        'next-path',
        # reverse('artist:artist-detail', args=[artist_pk]),
        reverse('artist:artist-detail', kwargs={'artist_pk': artist_pk}),
    )
    return redirect(next_path)

    # 여기로 데이터를 전달하는 form을
    #   artist_detail에 구현
    # 처리 완료 후, 'next'값이 전달되었으면 그 위치로
    # 아니면 artist_detail로 이동

    # artist_detail에 저장되어있는 youtube_videos목록을
    #   출력
    pass
