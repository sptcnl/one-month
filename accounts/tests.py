from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_signup_view():
    client = APIClient()
    url = reverse('signup')
    
    data = {
        "username": "JIN HO",
        "password": "1010qpqp",
        "nickname": "Mentos"
    }
    
    response = client.post(url, data, format='json')

    print(response.status_code)
    print(response.data)

    assert response.status_code == 201
    assert response.data['username'] == data['username']
    assert response.data['nickname'] == data['nickname']

@pytest.mark.django_db
def test_login_view_success():
    # 1. 테스트용 사용자 생성
    User.objects.create_user(username="testuser", password="testpassword")

    # 2. APIClient 초기화 및 로그인 요청
    client = APIClient()
    url = reverse('login')

    data = {
        "username": "testuser",
        "password": "testpassword"
    }

    response = client.post(url, data, format='json')

    print(response.status_code)
    print(response.data)

    # 3. 성공적인 응답 확인
    assert response.status_code == 200  # HTTP 200 OK

@pytest.mark.django_db
def test_login_view_invalid_credentials():
    # 1. 존재하지 않는 사용자로 로그인 시도
    client = APIClient()
    url = reverse('login')

    data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    response = client.post(url, data, format='json')

    print(response.status_code)
    print(response.data)

    # 2. 실패 응답 확인
    assert response.status_code == 401  # HTTP 401 Unauthorized

@pytest.mark.django_db
def test_login_view_missing_fields():
    # 1. 필수 필드 누락된 요청 시도
    client = APIClient()
    url = reverse('login')

    data = {
        "username": "",
        "password": ""
    }

    response = client.post(url, data, format='json')

    print(response.status_code)
    print(response.data)

    # 2. 실패 응답 확인
    assert response.status_code == 400  # HTTP 400 Bad Request