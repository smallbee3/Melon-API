from django.shortcuts import render

from .models import Album

# album, song에 대해서
# detail
# edit
# like-toggle
#  기능을 구현


def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(
        request,
        'album/album_list.html',
        context,
    )
