from django.shortcuts import redirect

from crawler.song import SongData
from song.models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    if request.method == 'POST':
        song_id = request.POST['song_id']
        song = SongData(song_id)
        song.get_detail()
        title = song.title
        genre = song.genre
        lyrics = song.lyrics

        song, _ = Song.objects.update_or_create(
            melon_id=song_id,
            defaults={
                'title': title,
                'genre': genre,
                'lyrics': lyrics,
            }
        )
        return redirect('song:song-list')
