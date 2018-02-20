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
        print(request.POST)
