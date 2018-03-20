from django.contrib import admin
from django.urls import path, include

from .. import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # artist/로 시작하는 path가
    # artist.urls모듈을 include하도록 설정
    path('', views.index, name='index'),

    path('', include('members.urls.views')),
    # path('login/', login_view, name='login'),
    # path('facebook-login/', facebook_login, name='facebookg-login'),
    # path('logout/', logout_view, name='logout'),
    # path('signup/', signup_view, name='signup'),

    path('artist/', include('artist.urls.views')),
    path('album/', include('album.urls')),
    path('song/', include('song.urls')),
]
