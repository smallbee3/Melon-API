from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Artist
from ...serializers import ArtistSerializer

# __all__ = (
#     'ArtistListView',
# )


class ArtistListView(APIView):
    # generics의 요소를 사용해서
    # ArtistListCreateView,
    # ArtistRetrieveUpdateDestroyView
    #   2개를 구현
    #   url과 연결
    #   postman api test 구현
    #   다 실행해보기
    #   pagination으로 5개 출력

    def get(self, request):
        print('request.user:', request.user)
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        print('request.user:', request.user)
        # return self.list(request, *args, **kwargs)
        # 이렇게 해도 되지만...
        # 뒷부분은 굳이 실행할 필요가 없기때문에..

        return super().get(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

# permission_classes = (
#     permissions.IsAuthenticatedOrReadOnly,
#     IsOwnerOrReadOnly,
# )