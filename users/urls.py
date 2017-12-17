from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

"""
    create token:  curl -X POST -d "email=vubon.roy@gmail.com&password=nothing1234" http://localhost:8000/test/api-token-auth/
    verify token: curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://localhost:8000/test/api-token-verify/

    
"""
