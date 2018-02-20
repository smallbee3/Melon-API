from datetime import datetime

import requests
from django.core.files import File
from django.shortcuts import redirect
from io import BytesIO

from crawler.artist import ArtistData
from ...models import Artist

__all__ = (
    'artist_add_from_melon',
)


def artist_add_from_melon(request):
    """
    1. artist_search_from_melon.html에
        form을 작성 (action이 현재 이 view로 올 수 있도록), POST메서드
            필요한 요소는 csrf_token과
                type=hidden으로 전달하는 artist_id값
                <input type="hidden" value="{{ artist_info.artist_id }}">
                button submit (추가하기)
    2. 작성한 form
    POST요청을 받음 (추가하기 버튼 클릭)
    request.POST['artist_id']

    artist_id를 사용해서
    멜론사이트에서 Artist에 들어갈 상세정보들을 가져옴

    name
    real_name
    nationality
    birth_date
    constellation
    blood_type
    intro

    1) 위 데이터를 그대로 HttpResponse로 출력해보기
    2) 잘 되면 채운 Artist를 생성, DB에 저장
    이후 artist:artist-list로 redirect

    :param request:
    :return:
    """
    if request.method == 'POST':
        artist_id = request.POST['artist_id']
        # 크롤링 코드. 자신이 작성한 크롤러를 사용해서 같은 데이터를 가져오면 됩니다
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

        # artist_id가 melon_id에 해당하는 Artist가 이미 있다면
        #   해당 Artist의 내용을 update
        # 없으면 Artist를 생성
        response = requests.get(url_img_cover)
        binary_data = response.content
        temp_file = BytesIO()
        temp_file.write(binary_data)
        temp_file.seek(0)

        artist, _ = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d'),
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )
        from pathlib import Path
        file_name = Path(url_img_cover).name
        artist.img_profile.save(file_name, File(temp_file))
        return redirect('artist:artist-list')
