from django.urls import path, include


urlpatterns = [

    path('artist/', include('artist.urls.apis')),
    # path('generics/artist', include('artist.urls.generics')),

    path('members/', include('members.urls.apis')),

]