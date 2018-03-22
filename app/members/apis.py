from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.urls import login
from rest_framework.views import APIView

from members.serializers import MemberSerialize, UserSerializer


class AuthTokenview(APIView):

    def post(self, request):

        # URL: /api/members/auth-token/
        # username, password를 받음
        # 유저인증에 성공했을 경우
        # 토큰을 생성하거나 잇으면 존재하는 걸 가져와서
        # Response로 돌려줌

        # 방법1 - 직접 모든 과정 구현
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



        # 방법2 - Serialize 사용
        # serializer = MemberSerialize(data=request.data)

        # attrs = AuthSerialize.validate(request.data)
        # return Response(serializer.data)

        # authenticate에 실패했을 때
        # raise APIException('authenticate failure')
        # raise AuthenticationFailed()


        # 방법2-2 - Serialize + 유효성 검사
        # serializer = AuthTokenSerializer(data=request.data)
        # if serializer.is_valid():
        #     user = serializer.validated_data['user']
        #     token, _ = Token.objects.get_or_create(user=user)
        #     data = {
        #         'token': token.key
        #     }
        #     return Response(data)


        # 방법2-3 - Serialize + 유효성 검사 + 예외처리를 위한 구조 변경
        #                               (예외발생시 raise_exception=True에서 바로 에러발생)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }
        return Response(data)


class MyUserDetail(APIView):

    # 3/22
    # request에 유저정보가 있는지 미들웨어 단에서 넣어줌.
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 
    def get(self, request):

        # data = {
        #     'user': UserSerializer(request.user).data
        # }
        # return Response(data)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)
