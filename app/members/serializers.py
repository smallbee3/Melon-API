from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


User = get_user_model()


class MemberSerialize(AuthTokenSerializer):

    def validate(self, attrs):

        attr = super().validate(self, attrs)

        token, _ = Token.objects.get_or_create(user=super().user)
        print('왔냐?')
        attrs['token'] = token.key
        print('왔다!')

        print('')
        print(token.key)
        print('')
        return attr


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
        )

