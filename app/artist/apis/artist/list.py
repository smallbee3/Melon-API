from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Artist
from ...serializers import ArtistSerializer

# __all__ = (
#     'ArtistListView',
# )


class ArtistListView(APIView):
    """
    3/19 과제
    generics의 요소를 사용해서
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView
      2개를 구현
      url과 연결
      postman api test 구현
      다 실행해보기
      pagination으로 5개 출력
    """


    def get(self, request):
        """
        3/20 오전 수업 실습 - 멘붕
        1. 특정 유저의 Token을 생성
        2. TokenAuthentication을 사용하도록 REST_FRAMEWORK설정
        3. Postman의 HTTP Header 'Authorization'에
              Token <value> <- 지정
        4. 요청 후 request.user가 정상적으로 출력되는지 확인
        """
        print('request.user:', request.user)

        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class ArtistListCreateView(generics.ListCreateAPIView):
    """
    3/20 오전 수업 실습 - 멘붕
    1. 특정 유저의 Token을 생성
    2. TokenAuthentication을 사용하도록 REST_FRAMEWORK설정
    3. Postman의 HTTP Header 'Authorization'에
          Token <value> <- 지정
    4. 요청 후 request.user가 정상적으로 출력되는지 확인
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    pagination_class = StandardResultsSetPagination

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request, *args, **kwargs):
        print('request.user:', request.user)
        return super().get(request, *args, **kwargs)

        # return self.list(request, *args, **kwargs)
        # 이렇게 해도 되지만...
        # 뒷부분은 굳이 실행할 필요가 없기때문에..


    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

# permission_classes = (
#     permissions.IsAuthenticatedOrReadOnly,
#     IsOwnerOrReadOnly,
# )