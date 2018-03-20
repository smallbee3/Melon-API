from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.urls import login
from rest_framework.views import APIView

from members.serializers import MemberSerialize


class AuthTokenview(APIView):

    def post(self, request):

        # URL: /api/members/auth-token/
        # username, password를 받음
        # 유저인증에 성공했을 경우
        # 토큰을 생성하거나 잇으면 존재하는 걸 가져와서
        # Response로 돌려줌

        # username = request.data['username']
        # password = request.data['password']
        # RESTFramework 쓸때는 data를 쓰는 것을 추천.

        # AuthTokenSerializer를 사용해서 위 로직을 실행
        #
        # username = request.data.get('username')
        # password = request.data.get('password')
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     token, _ = Token.objects.get_or_create(user=user)
        #     data = {
        #         'token': token.key,
        #     }
        #     return Response(data)
        #
        # # authenticate에 실패했을 때
        # # raise APIException('authenticate failure')
        # raise AuthenticationFailed()

        serializer = MemberSerialize(request.data)

        # attrs = AuthSerialize.validate(request.data)
        return Response(serializer.data)

        # authenticate에 실패했을 때
        # raise APIException('authenticate failure')
        # raise AuthenticationFailed()



        # serializer = AuthTokenSerializer(data=request.data)
        # if serializer.is_valid():
        #     user = serializer.validated_data['user']
        #     token, _ = Token.objects.get_or_create(user=user)
        #     data = {
        #         'token': token.key
        #     }
        #     return Response(data)

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key
        }
        return Response(data)