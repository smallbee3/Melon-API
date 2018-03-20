from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.urls import login
from rest_framework.views import APIView


class AuthTokenview(APIView):
    def post(self, request):

        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        token_key = '키없음'
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            token_key = token.key
        return Response(token_key)

        # URL: /api/members/auth-token/
        # username, password를 받음
        # 유저인증에 성공했을 경우
        # 토큰을 생성하거나 잇으면 존재하는 걸 가져와서
        # Response로 돌려줌