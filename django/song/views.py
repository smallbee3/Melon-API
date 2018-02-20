from django.db.models import Q
from django.shortcuts import render

from .models import Song


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    return render(
        request,
        'song/song_list.html',
        context,
    )


def song_search(request):
    """
    사용할 URL: song/search/
    사용할 Template: templates/song/song_search.html
        form안에
            input한개, button한개 배치

    1. song/urls.py에 URL작성
    2. templates/song/song_search.html작성
        {% extends %} 사용할 것
        form배치 후 method는 POST, {% csrf_token %}배치
    3. 이 함수에서 return render(...)
        *아직 context는 사용하지 않음

    - GET, POST분기
    1. input의 name을 keyword로 지정
    2. 이 함수를 request.method가 'GET'일 때와 'POST'일 때로 분기
    3. request.method가 'POST'일 때
        request.POST dict의 'keyword'키에 해당하는 값을
        HttpResponse로 출력
    4. request.method가 'GET'일 때
        이전에 하던 템플릿 출력을 유지

    - Query filter로 검색하기
    1. keyword가 자신의 'title'에 포함되는 Song쿼리셋 생성
    2.  위 쿼리셋을 'songs'변수에 할당
    3. context dict를 만들고 'songs'키에 songs변수를 할당
    4. render의 3번째 인수로 context를 전달
    5. template에 전달된 'songs'를 출력
        song_search.html을 그대로 사용
    :param request:
    :return:
    """
    # Song과 연결된 Artist의 name에 keyword가 포함되는 경우
    # Song과 연결된 Album의 title에 keyword가 포함되는 경우
    # Song의 title에 keyword가 포함되는 경우
    #   를 모두 포함(or -> Q object)하는 쿼리셋을 'songs'에 할당

    # songs_from_artists
    # songs_from_albums
    # songs_from_title
    #  위 세 변수에 더 위의 조건 3개에 부합하는 쿼리셋을 각각 전달
    #  세 변수를 이용해 검색 결과를 3단으로 분리해서 출력
    #  -> 아티스트로 검색한 노래 결과, 앨범으로 검색한 노래 결과, 제목으로 검색한 노래 결과
    context = {
        'song_infos': [],
    }
    keyword = request.GET.get('keyword')
    if keyword:
        song_infos = (
            ('아티스트명', Q(album__artists__name__contains=keyword)),
            ('앨범명', Q(album__title__contains=keyword)),
            ('노래제목', Q(title__contains=keyword)),
        )
        for type, q in song_infos:
            context['song_infos'].append({
                'type': type,
                'songs': Song.objects.filter(q),
            })




    context['type'] = 'ASDF'
    return render(request, 'song/song_search.html', context)
