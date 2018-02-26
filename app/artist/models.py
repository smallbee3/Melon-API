from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.db import models

from crawler.artist import ArtistData
from utils.file import download, get_buffer_ext


class ArtistManager(models.Manager):
    def update_or_create_from_melon(self, artist_id):
        artist = ArtistData(artist_id)
        artist.get_detail()
        name = artist.name
        url_img_cover = artist.url_img_cover
        real_name = artist.personal_information.get('본명', '')
        nationality = artist.personal_information.get('국적', '')
        birth_date_str = artist.personal_information.get('생일', '')
        constellation = artist.personal_information.get('별자리', '')
        blood_type = artist.personal_information.get('혈액형', '')

        # blood_type과 birth_date_str이 없을때 처리할것

        # 튜플의 리스트를 순회하며 blood_type을 결정
        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
        else:
            # break가 발생하지 않은 경우
            # (미리 정의해놓은 혈액형 타입에 없을 경우)
            # 기타 혈액형값으로 설정
            blood_type = Artist.BLOOD_TYPE_OTHER

        artist, artist_created = self.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(
                    birth_date_str, '%Y.%m.%d') if birth_date_str else None,
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )
        # img_profile필드에 저장할 파일확장자를 바이너리 데이터 자체의 MIME_TYPE에서 가져옴
        # 파일명은 artist_id를 사용
        temp_file = download(url_img_cover)
        file_name = '{artist_id}.{ext}'.format(
            artist_id=artist_id,
            ext=get_buffer_ext(temp_file),
        )
        # artist.img_profile필드의 save를 따로 호출, 이름과 File객체를 전달
        #   (Django)File객체의 생성에는 (Python)File객체를 사용,
        #           이 때 (Python)File객체처럼 취급되는 BytesIO를 사용
        if artist.img_profile:
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))
        return artist, artist_created


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = 'x'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )
    melon_id = models.CharField(
        '멜론 Artist ID',
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='artist',
        blank=True,
    )
    name = models.CharField(
        '이름',
        max_length=50,
    )
    real_name = models.CharField(
        '본명',
        max_length=30,
        blank=True,
    )
    nationality = models.CharField(
        '국적',
        max_length=50,
        blank=True,
    )
    birth_date = models.DateField(
        '생년월일',
        blank=True,
        null=True,
    )
    constellation = models.CharField(
        '별자리',
        max_length=30,
        blank=True,
    )
    blood_type = models.CharField(
        '혈액형',
        max_length=1,
        choices=CHOICES_BLOOD_TYPE,
        blank=True,
    )
    intro = models.TextField(
        '소개',
        blank=True,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ArtistLike',
        related_name='like_artists',
        blank=True,
    )

    objects = ArtistManager()

    def __str__(self):
        return self.name

    def toggle_like_user(self, user):
        """
        자신의 like_users에 주어진 user가 존재하지 않으면
            like_users에 추가한다
        이미 존재할 경우에는 없앤다
        :param user:
        :return:
        """
        # # 자신이 artist이며, 주어진 user와의 ArtistLike의 QuerySet
        # query = ArtistLike.objects.filter(artist=self, user=user)
        # # QuerySet이 존재할 경우
        # if query.exists():
        #     # 지워주고 False반환
        #     query.delete()
        #     return False
        # # QuerySet이 존재하지 않을 경우
        # else:
        #     # 새로 ArtistLike를 생성하고 True반환
        #     ArtistLike.objects.create(artist=self, user=user)
        #     return True

        # 자신이 'artist'이며 user가 주어진 user인 ArtistLike를 가져오거나 없으면 생성
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        # 만약 이미 있었을 경우 (새로 생성되지 않았을 경우)
        if not like_created:
            # Like를 지워줌
            like.delete()
        # 생성여부를 반환 (Toggle후 현재 상태에 대한 True/False와 같은 결과)
        return like_created


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
