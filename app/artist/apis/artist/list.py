from django.http import JsonResponse

from artist.models import Artist


def artist_list(request):
    # localhost:8000/api/artist/
    artists = Artist.objects.all()
    data = {
        'artists': artists,
    }
    return JsonResponse(data)

# /artist/       -> artist.urls.views
# /api/artist/   -> artist.urls.apis

# /album/        -> album.urls.views
# /api/album/    -> album.urls.apis
