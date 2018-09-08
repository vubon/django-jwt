"""
Token analysis
"""
import datetime

from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from users.models import User

from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, jwt_response_payload_handler
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer

from users.decorators import check_user, authorize_check

token_decoder = api_settings.JWT_DECODE_HANDLER
token_encoded = api_settings.JWT_ENCODE_HANDLER


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


class RefreshToken(APIView):
    """
        - Checking serializer valid or not
        - if not return 401 .e.i unauthorized, whatever error in serializer it will return status code 401
        - if pass the serializer, decoded the token and check authorized or not the user
        - If not pass then return 401
        - if pass then get refresh a token and decoded the token again and add extra field authorize
        -  and return a new token
    """
    serializer_class = RefreshJSONWebTokenSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            decoded_token = token_decoder(request.data['token'])
            user_response = authorize_check(decoded_token)

            if user_response:
                user = User.objects.get(email=decoded_token['email'])
                get_token = serializer.object.get('token')

                dec_token = token_decoder(get_token)
                print(dec_token)
                dec_token['authorize'] = decoded_token['authorize']

                token = token_encoded(dec_token)

                response_data = jwt_response_payload_handler(token, user, request)

                response = Response(response_data, status=200)
                if api_settings.JWT_AUTH_COOKIE:
                    expiration = (datetime.datetime.now() + api_settings.JWT_EXPIRATION_DELTA)
                    response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
                return response

            return Response(status=401)
        else:
            return Response(serializer.errors, status=401)
