from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User클래스를 정의
    # INSTALLED_APPS에 members application추가
    # AUTH_USER_MODEL 정의 (AppName.ModelClassName)
    # 모든 application들의 migrations폴더내의 Migration파일 전부 삭제
    # makemigrations -> migrate

    # 데이터베이스에 member_user 테이블이 생성되었는지 확인
    pass
