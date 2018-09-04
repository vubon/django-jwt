# JWT Deep Dive
I am not going to dicuss about basic concept of JWT. If need please visit this website 
[JWT TOKEN](https://getblimp.github.io/django-rest-framework-jwt/)

## Generate a token 
```code
URL: URI/api/v1/api-token-auth/
Method: POST
```
```json
{
  "email": "vubon.roy@gmail.com",
  "password": "xxxxx",
  "authorize": true
}
```
authorize is a extra field and we will add this field in token . 


How to add extra Field into your token ?
- 
```python
import datetime
from django.utils.decorators import method_decorator
from rest_framework.response import Response

# JWT token classes and methods 
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler
token_decoder = api_settings.JWT_DECODE_HANDLER
token_encoded = api_settings.JWT_ENCODE_HANDLER

from users.decorators import check_user

class ObtainToken(ObtainJSONWebToken):

    @method_decorator(check_user)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            token = serializer.object.get('token')
            decoded_token = token_decoder(token)
            decoded_token['authorize'] = request.data['authorize']
            token = token_encoded(decoded_token)
            response_data = jwt_response_payload_handler(token, user, request)

            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.datetime.now() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response

        return Response(serializer.errors, status=401)

```
