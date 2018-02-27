from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # User클래스를 정의
    # INSTALLED_APPS에 members application추가
    # AUTH_USER_MODEL 정의 (AppName.ModelClassName)
    # 모든 application들의 migrations폴더내의 Migration파일 전부 삭제
    # makemigrations -> migrate
    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )

    # 데이터베이스에 member_user 테이블이 생성되었는지 확인
    def toggle_like_artist(self, artist):
        """
        이 User와 특정 Artist를 연결하는
        중개모델인 ArtistLike인스턴스를
            없을경우 생성, 있으면 삭제하는 메서드
        :param artist:
        :return:
        """
        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created
