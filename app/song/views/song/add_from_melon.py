from django.shortcuts import redirect

from artist.models import Artist
from crawler.song import SongData
from song.models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    if request.method == 'POST':
        song_id = request.POST['song_id']
        Song.objects.update_or_create_from_melon_id(song_id)
        return redirect('song:song-list')
