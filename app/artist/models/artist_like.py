from datetime import datetime

from django.conf import settings
from django.db import models

from .artist import Artist

__all__ = (
    'ArtistLike',
)


class ArtistLike(models.Model):
    # Artist와 User(members.User)와의 관계를 나타내는 중개모델
    # settings.AUTH_USER_MODEL

    # 다 작성 후에
    # 임의의 유저에서 좋아하는 Artist추가해보기
    # 임의의 Artist에서 좋아하고있는 유저 추가해보기
    artist = models.ForeignKey(
        Artist,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_artist_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('artist', 'user'),
        )

    def __str__(self):
        return 'ArtistLike (User: {user}, Artist: {artist}, Created: {created})'.format(
            user=self.user.username,
            artist=self.artist.name,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )
