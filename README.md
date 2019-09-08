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
        - 각 모델에서 발생하는 DB 변경 점 알림

## DB
 **1. Models**
    
    ```
    User
    Image
    Comment
    Like
    Notification
    ```
 **2. Command**

    > python manage.py migrate

    > python manage.py makemigrations

        makimigrations 은 장고에서 제공하는 모델(models.py)의 변경사항들을 감지하고 기록하는 역할
        
        migrate 는 그러한 기록된 파일들과 설정값들을 읽어서 그 변경사항을 DB에 반영하는 역할을 한다.
    > python manage.py migrate & python manage.py makemigrations
    >> 위 처럼 두 명령어를 한 번에 실행 가능 for mac & linux


## Authentication

## JWT
>RN 에서 Cookie 관리가 쉽지 않아서(못할건 아니지만 이게 편해서) JWT 를 이용 

> pip install django-rest-auth

**1. INSTALLED_APPS 에 추가**

    ```
    INSTALLED_APPS = (
        ...,
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'rest_auth.registration',
    )
    ```
**2. Cafeteria 의 urls.py 에 추가**

    ```
    urlpatterns = [
        ...,
        url(r'^rest-auth/', include('rest_auth.urls')), // rest_auth start
        url(r'^rest-auth/registration/', include('rest_auth.registration.urls')) // rest_auth login url
    ] 
    ```
    해당 url 추가 후 아래 명령어 실행
    > python manage.py migrate

**3. JWT Token 발행**
    
> jwt 테스트를 위해 크롬앱 postman 설치 사용법은 [이곳](https://meetup.toast.com/posts/107)을 참조

    ```
    1. localhost:[hostnumber]/rest-auth/login/ // 주소 끝에 "/" 를 빼면 에러 발생 주의
        - username, email, password (POST 값) 
        - 발행 된 토큰 복사
    ```

**4. JWT Token 인증**
   ```
    1. 복사한 토큰 헤더에 추가
    2. localhost:[hostnumber]/[myurl] 테스트 확인
   ```

**5. Social Login for kakao (facebook, google)**
> django allauth 이용. 자세한 내용은 [이곳](https://django-allauth.readthedocs.io/en/latest/installation.html)을 참조

1) Django setting
   - settings.py
       ```
       INSTALLED_APPS = (
           # The following apps are required:
           'django.contrib.auth',
           'django.contrib.messages',
           'django.contrib.sites',
           'allauth',
           'allauth.account',
           'allauth.socialaccount',
           
           # ... include the providers you want to enable:
           'allauth.socialaccount.providers.kakao',
       )
       ```
   - urls.py
       ```
       urlpatterns = [
           ...
           path("login/kakao/", view=views.KakaoLogin.as_view(), name='kakao_login')
           ...
       ]
       ```
   > python manage.py makemigrations && python manage.py migrate
   >> 모두 추가 후 해당 명령어 실행하여 migrate 해준다.

    - django panel
        ```
        어드민 패널에서 소셜어플리케이션을 추가할때
        카카오는 secret key (발급 받을 수는 있음) 가 없으므로 rest api 키를 secret key 값에 넣어준다(사실 아무거나 넣어도 무관..)
        ```

2) Kakao developer 
    > 아래 순서를 따른다.
    - https://developers.kakao.com/ 로그인
    - 좌측 상단 앱 만들
    - 아이콘 (선택), 앱 이름, 회사명 입력 후 생성
    - 앱 설정 -> 사용자 관리 -> 로그인 Redirect URI 에 개발 서버 등록
    - 카카오 REST API [도구](https://developers.kakao.com/docs/restapi/tool)를 이용해 임시토큰 생성
    - 위에서 설정한 url (localhost:8000/login/kakao/) 으로 이동 후 생성한 임시토큰 값 전송

> kakao 뿐만 아니라 소셜 로그인 대부분이 위와 같은 방법을 따른다.
> 기회가 되면 타 소셜로그인 방법도 올릴 예정

## django React block 설정 해제

1. proxy the request from 3000 to 8000
    > proxy 를 :3000 에서 :8000으로 보냄
2. install django-cors-headers
    > django-cors-headers 설치
3. Add 'corsheaders' to INSTALL_APPS
    > INSTALL_APPS 에 'corsheaders' 추가
4. Add 'corsheaders.middleware.CoreMiddleware' before 'CommonnMiddleware'
    > CommonnMiddleware' 앞에 'corsheaders.middleware.CoreMiddleware'를 추가
5. Add CORS_ORIGIN_ALLOW_ALL = True on base settings
    > base setting 에 CORS_ORIGIN_ALLOW_ALL = True 추가
6. Make Djagno load the bunndles as static files with 'str(ROOT_DIR.path('fronted','build','static'))'
    > Djagno 에서 'str (ROOT_DIR.path ('fronted ','build ','static '))'을 사용하여 번들을 static 파일로로드
7. Create a views.py file on 'cafeteria' folder
    > cafeteria 폴더에 view 추가
8. Create ReactAppView that reads the file.
    > ReactAppView 작성
9.  Add the ReactAppView as a URL
    > ReactAppView를 URL로 추가








    




    
    
    