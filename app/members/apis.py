from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.urls import login
from rest_framework.views import APIView

from members.serializers import UserSerializer, AccessTokenSerializer
# from members.serializers import MemberSerialize


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

    def get(self, request):

        # data = {
        #     'user': UserSerializer(request.user).data
        # }
        # return Response(data)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AuthTokenForFacebookAccessTokenView(APIView):
    def post(self, request):
        """
        access_token이라는 이름으로 1개의 데이터가 전달됨
        해당 데이터를 가지고 AccessTokenSerializer에서 validation
        이 과정에서 authenticate가 이루어지며
        authenticate에서 페이스북과 통신해서 유저정보를 받아옴
        받아온 유저정보와 일치하는 유저가 있으면 해당 유저를, 없으면 생성해서 반환
        리턴된 유저는 serializer의 validated_data의 'user'라는 키에
        """

        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 위 is_valid를 통해 AccessTokenSerializer의 validate 함수에서
        # raise serializers.ValidationError가 발생하면
        # raise_exception=True옵션으로 인해 바로 에러가 발생하고
        # 하단의 과정은 생략됨. (right?)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)



        # def get_user_info(user_access_token):
        #     """
        #     User access token을 사용해서
        #     GraphAPI의 'User'항목을 리턴
        #         (엔드포인트 'me'를 사용해서 access_token에 해당하는 사용자의 정보를 가져옴)
        #     :param user_access_token: 정보를 가져올 Facebook User access token
        #     :return: User정보 (dict)
        #     """
        #     params = {
        #         'access_token': user_access_token,
        #         'fields': ','.join([
        #             'id',
        #             'name',
        #             'picture.width(2500)',
        #             'first_name',
        #             'last_name',
        #         ])
        #     }
        #     response = requests.get('https://graph.facebook.com/v2.12/me', params)
        #     response_dict = response.json()
        #     return response_dict
        #
        # access_token = request.data.get('access_token')
        # user_info = get_user_info(access_token)
        #
        # serializer = AccessTokenSerializer()
        #
        #
        #
        # print('')
        # # print(request.data)
        # # print(access_token)
        # # print('')
        # return Response(user_info)
