import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from math import ceil
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from artist.apis import ArtistListCreateView
from artist.models import Artist
from artist.serializers import ArtistSerializer


class ArtistListTest(APITestCase):
    # 동일하게 사용되는 상수를 클래스 속성으로 지
    MODEL = Artist
    VIEW = ArtistListCreateView
    PATH = '/api/artist/'
    VIEW_NAME = 'apis:artist:artist-list'
    PAGINATION_COUNT = 5

    def test_reverse(self):
        # 기대하는 URL path: /api/artist/
        # artist-list에 해당하는 URL name을 reverse했을 때,
        # 우리가 기대하는 URL path와 일치하는지 테스트
        #   -> Django url reverse으로 검색
        f"""
        Artist List에 해당하는 VIEW_NAME을 reverse한 결과가 기대 PATH와 같은지 검사
            VIEW_NAME: {self.VIEW_NAME}
            PATH:      {self.PATH}
        """

        # url_name = 'apis:artist:artist-list'
        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_resolve(self):
        # 기대하는 View function: ArtistListCreateView.as_view()
        # 기대하는 URL names: 'apis:artist:artist-list'

        # artist-list에 해당하는 URL path를 resolve했을 때,
        # 1. ResolverMatch obj의 func의 __name__속성이
        #    우리가 기대하는 View function의 __name__속성과 같은지
        # 2. ResolverMatch obj의 view_name이 우리가 기대하는 URL name과 같은지
        #   테스트
        #   -> Django url resolve, Django resolver match 검
        f"""
        Artist List에 해당하는 PATH를 resolve한 결과의 func와 view_name이
        기대하는 View.as_view()와 VIEW_NAME과 같은지 검사
            PATH:       {self.PATH}
            VIEW_NAME:  {self.VIEW_NAME}
        """

        # path = '/api/artist/'
        resolver_match = resolve(self.PATH)
        self.assertEqual(
            resolver_match.func.__name__,
            self.VIEW.as_view().__name__,
        )

        self.assertEqual(
            resolver_match.view_name,
            self.VIEW_NAME,
        )

    def test_artist_list_count(self):

        num = random.randrange(1, 10)
        for i in range(num):
            Artist.objects.create(name=f'Artist{i}')

        print(num)

        response = self.client.get(self.PATH)
        # artist_num = response.data
        # self.assertEqual(Artist.objects.count(), len(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'],
            self.MODEL.objects.count(),
        )

        print(response.data['count'])
        self.assertEqual(
            response.data['count'],
            num,
            # num이란 개수 만큼 만드니까
            # 이것도 테스
        )

        # self.client에 get요청
        # response.data를 사용

        # artist-list요청 시 알 수 있는 전체 Artist개수가 기대값과 같은지 테스트
        #   (테스트용 Artist를 여러개 생성해야 함)

    def test_artist_list_pagination(self):

        num = 13
        for i in range(num):
            Artist.objects.create(name=f'Artist{i + 1}')

        # artist-list요청시 pagination이 잘 적용되어있는지 테스트
        # pagination된 'result'내부의 값이
        # 실제 QuerySet을 Serialize한 결과와도 같은지 테스트
        # math.ceil <- 소수점 올림
        response = self.client.get(self.PATH, {'page': 1})

        # 응답코드 200 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # 3/26 과제 (1) - pagination
        # for문을 사용해서, 아래의 로직이
        #   페이지네이션 된 모든 page들에 요청 후 results값을 확인하도록 구성

        it = iter(response.data['results'][::5])

        for i in range(ceil(num/self.PAGINATION_COUNT)):
            self.assertEqual(
                len(next(it)),
                self.PAGINATION_COUNT,
            )
            self.assertEqual(
                response.data['results'],
                ArtistSerializer(Artist.objects.all()[:5], many=True).data
            )

        # 'results'키에 5개의 데이터가 배열로 전달되는지 확인
        # self.assertEqual(
        #     len(response.data['results']),
        #     self.PAGINATION_COUNT,
        # )
        #
        # 'results'키에 들어있는 5개의 Artist가 serialize되어있는 결과가
        # 실제 QuerySet을 serialize한 결과와
        # self.assertEqual(
        #     response.data['result'],
        #     ArtistSerializer(Artist.objects.all()[:5], many=True).data
        # )


class ArtistCreateTest(APITestCase):
    PATH = '/api/artist/'

    User = get_user_model()
    u1 = User.objects.first()
    TOKEN = Token.objects.get(user=u1)

    print(TOKEN.key)

    def test_create_post(self):

        img_file = open('static/test/hackerton.png', 'rb')

        print(img_file)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.TOKEN.key)
        response = self.client.post(self.PATH, {'img_profile': img_file, 'name': 'hac'})

        a = Artist.objects.last()
        print(a)
        self.assertEqual(
            a.img_profile,
            img_file,
        )

        # 3/26 과제 (2) - ArtistCreate
        # (2-1)
        # /static/test/hackerton.png에 있는 파일을 사용해서
        # 나머지 데이터를 채워서 Artist객체를 생성
        
        # 파일을 이진데이터로 읽어서 생성하면 됩니다.
        
        # 이진데이터 모드로 연 '파일 객체'를
        # 생성할 Aritst의 '파일 필드 명'으로 전달
        # self.client.post(URL, {'img_profile': <파일객체>})

        # (2-2)
        # authenticate를 못했는데 넣어주세요.
        # 세션때문에 이걸 스면안되고 credentials라고 토큰값을 전달하는 법이 있어요.
        # create하는 것은 로그인한 유저만 해야되는 테스트를 짜보세요.
