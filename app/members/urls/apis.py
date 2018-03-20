from django.urls import path, include

from members.apis import (
    AuthTokenview,
)


urlpatterns = [
    path('auth-token/', AuthTokenview.as_view()),
]
