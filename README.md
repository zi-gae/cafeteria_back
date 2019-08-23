# Cafeteria app

## with Django & React & RN

# django
    python 3.7
    django 2.2
    
### Setting
    
    set: Cookiecutter 를 기본설정으로 따름
    DB: postgress

### Install package
    rest_framework
    rest_framework.authtoken
    rest_auth
    rest_auth.registration

## App
    1. Users
       - 회원가입
       - 정보변경
    2. Images
        - 게시글
        - Like & UnLike
        - UserProfile
        - Comment
    3. Notification 
        - Images 모델에서 발생하는 DB 변경 알림들

## DB
#### Models
    User
    Image
    Comment
    Like
    Notification
#### Command

> python manage.py migrate

> python manage.py makemigrations

    makimigrations 은 장고에서 제공하는 모델(models.py)의 변경사항들을 감지하고 기록하는 역할
    
    migrate 는 그러한 기록된 파일들과 설정값들을 읽어서 그 변경사항을 DB에 반영하는 역할을 한다.
> python manage.py migrate & python manage.py makemigrations
>> 위 처럼 두 명령어를 한 번에 실행 가능 for mac & linux


## Authentication

#### JWT
>RN 에서 Cookie 관리가 쉽지 않아서(못할건 아니지만 이게 편해서) JWT 를 이용 

> pip install django-rest-auth

1. INSTALLED_APPS 에 추가
    ```
    INSTALLED_APPS = (
        ...,
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'rest_auth.registration',
    )
    ```
2. Cafeteria 의 urls.py 에 추가
    ```
    urlpatterns = [
        ...,
        url(r'^rest-auth/', include('rest_auth.urls')), // rest_auth start
        url(r'^rest-auth/registration/', include('rest_auth.registration.urls')) // rest_auth login url
    ] 
    ```
    해당 url 추가 후 아래 명령어 실행
    > python manage.py migrate

3. JWT Token 발행
    
    > jwt 테스트를 위해 크롬앱 postman 설치 사용법은 [참조](https://meetup.toast.com/posts/107)
    ```
    1. localhost:[hostnumber]/rest-auth/login/ // 주소 끝에 "/" 를 빼면 에러 발생 주의
        - username, email, password (POST 값) 
        - 발행 된 토큰 복사
    ```

4. JWT Token 인증
   ```
    1. 복사한 토큰 헤더에 추가
    2. localhost:[hostnumber]/[myurl] 테스트 확인
   ```



    




    
    
    