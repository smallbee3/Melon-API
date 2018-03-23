import requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


User = get_user_model()


# class MemberSerialize(AuthTokenSerializer):
#
#     def validate(self, attrs):
#
#         attr = super().validate(self, attrs)
#
#         token, _ = Token.objects.get_or_create(user=super().user)
#         print('왔냐?')
#         attrs['token'] = token.key
#         print('왔다!')
#
#         print('')
#         print(token.key)
#         print('')
#         return attr


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
        )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        if access_token:
            user = authenticate(access_token=access_token)
            if not user:
                raise serializers.ValidationError('액세스 토큰이 올바르지 않습니다.')
        else:
            raise serializers.ValidationError('엑세스 토큰이 필요합니다.')

        attrs['user'] = user
        return attrs

            # params = {
            #     'access_token': access_token,
            #     'fields': ','.join([
            #         'id',
            #         'name',
            #         'picture.width(2500)',
            #         'first_name',
            #         'last_name',
            #     ])
            # }
            # response = requests.get('https://graph.facebook.com/v2.12/me', params)
            # response_dict = response.json()
            # facebook_id = response_dict['id']
            # user, _ = User.objects.get_or_create(username=facebook_id)



