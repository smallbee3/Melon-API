import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import redirect

User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    # GET parameter가 왔을 것으로 가정
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')


def facebook_login_backup(request):
    # code로부터 AccessToken 가져오기
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    # 페이스북로그인 버튼을 누른 후, 사용자가 승인하면 redirect_uri에 GET parameter로 'code'가 전송됨
    # 이 값과 client_id, secret을 사용해서 Facebook서버에서 access_token을 받아와야 함
    code = request.GET['code']
    # 이전에 페이스북 로그인 버튼을 눌렀을 때 'code'를 다시 전달받은 redirect_uri값을 그대로 사용
    redirect_uri = 'http://localhost:8000/facebook-login/'

    # 아래 엔드포인트에 GET요청을 보냄
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)
    # 전송받은 결과는 JSON형식의 텍스트. requests가 제공하는 JSON 디코더를 사용해서
    # JSON텍스트를 Python dict로 변환해준다
    response_dict = response.json()
    # 값 출력해보기
    # access_token: EAAXhjYZBChTABANYrACAcZCZCxgrwTYZAIW0j5B5XsSpQBVkWPD8GCYBlwZAyvOAH6w9VdTVzsjVObhtald135JZBWVQwkqLQebfwdE1mbQjFC3vvRYlZBM1i44tAyIyJJWQzVF8bK1UgCOHt1Vd5zi4S7Njfcmziat1rTicC2V4wZDZD
    # token_type: bearer
    # expires_in: 5182104
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    # GraphAPI의 me 엔드포인트에 GET요청 보내기
    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ])
    }
    response = requests.get(url, params)
    response_dict = response.json()
    # {
    # 'id': '796434757212474',
    # 'name': '이한영',
    # 'picture':
    #   {'data': {
    #       'height': 1024,
    #       'is_silhouette': False,
    #       'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/27164517_781031958752754_5931684880075482184_o.jpg?oh=6997505c279ac83622a253bf1014fd88&oe=5B089210',
    #       'width': 1024}
    #   },
    # 'first_name': '한영',
    # 'last_name': '이'
    # }
    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_picture = response_dict['picture']['data']['url']

    # facebook_id가 username인 User가 존재할 경우
    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    # 존재하지 않으면 새 유저를 생성
    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    # 해당 유저를 로그인 시킴
    login(request, user)
    return redirect('index')
