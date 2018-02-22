from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from django.core.files import File
from django.db import models

from crawler.artist import ArtistData


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

        # url_img_cover는 이미지의 URL
        response = requests.get(url_img_cover)
        # requests에 GET요청을 보낸 결과의 Binary data
        binary_data = response.content
        # 파일처럼 취급되는 메모리 객체 temp_file를 생성
        temp_file = BytesIO()
        # temp_file에 이진데이터를 기록
        temp_file.write(binary_data)
        # 파일객체의 포인터를 시작부분으로 되돌림
        temp_file.seek(0)

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
        # img_profile필드에 저장할 파일명을 전체 URL경로에서 추출 (Path라이브러리)
        file_name = Path(url_img_cover).name
        # artist.img_profile필드의 save를 따로 호출, 이름과 File객체를 전달
        #   (Django)File객체의 생성에는 (Python)File객체를 사용,
        #           이 때 (Python)File객체처럼 취급되는 BytesIO를 사용
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

    objects = ArtistManager()

    def __str__(self):
        return self.name
