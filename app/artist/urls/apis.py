from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .. import apis

app_name = 'artist'
urlpatterns = [
    # path('', apis.artist_list, name='artist-list'),
    path('drf/', apis.ArtistListView.as_view(), name='artist-list2'),
    path('', apis.ArtistListCreateView.as_view(), name='artist-list'),
    path('<int:pk>/', apis.ArtistRetrieveUpdateDestroyView.as_view(), name='artist-detail'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
