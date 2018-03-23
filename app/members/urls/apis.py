from django.urls import path, include

from members.apis import (
    AuthTokenview,
    MyUserDetail,
    AuthTokenForFacebookAccessTokenView,
)


urlpatterns = [
    path('auth-token/', AuthTokenview.as_view()),
    path('info/', MyUserDetail.as_view()),
    path('facebook-auth-token/', AuthTokenForFacebookAccessTokenView.as_view())
]
