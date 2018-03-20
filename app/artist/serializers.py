from rest_framework import serializers

from artist.models.artist_youtube import ArtistYouTube
from members.serializers import UserSerializer
from .models import Artist


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistYouTube
        fields = (
            'youtube_id',
            'title',
            'url_thumbnail',
        )


class ArtistSerializer(serializers.ModelSerializer):

    like_users = UserSerializer(many=True, read_only=True)

    youtube_videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'
        # fields = (
        #     'melon_id',
        #     'img_profile',
        #     'name',
        #     'like_users',
        # )

