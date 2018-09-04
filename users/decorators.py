import json

from django.shortcuts import get_object_or_404

from users.models import User
from django.contrib.auth import authenticate

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from account.response_messages import *


# create custom 401 Unauthorized
class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def check_user(func):
    """
    Decorator to authenticate a user
    :param: func: support user checking for token
    """

    def wrapper(request, *args, **kwargs):

        if "email" not in request.data or "password" not in request.data:
            return HttpResponseBadRequest(json.dumps({"message": DONT_KNOW_ANYTHING}))

        if "email" in request.data and "password" in request.data:
            username = request.data.get("email", request.user)
            password = request.data["password"]

            # check user is registered
            if not User.objects.filter(email=username).exists():
                return HttpResponseBadRequest(json.dumps({"message": USER_NOT_FOUND}))

            # If user is activated or not
            if not User.objects.get(email=username).is_active:
                return HttpResponseBadRequest(json.dumps({"message": INACTIVATED_USER}))

            # checking authorized or not
            if not User.objects.get(email=username).authorize:
                return HttpResponseBadRequest(json.dumps({"message": NOT_AUTHORIZED}))

            # Check user credentials
            user = authenticate(email=username, password=password)
            if not user:
                return HttpResponseUnauthorized(json.dumps({"message": UNABLE_TO_LOGIN}))
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest(json.dumps({"message": INVALID_DATA}))

    return wrapper


def authorize_check(data):

    if "email" not in data:
        return HttpResponseBadRequest(json.dumps({"message": DONT_KNOW_ANYTHING}))

    if "email" in data:
        username = data.get("email")

        # check user is registered
        if not User.objects.filter(email=username).exists():
            return False

        # If user is activated or not
        if not User.objects.get(email=username).is_active:
            return False

        # checking authorized or not
        if not User.objects.get(email=username).authorize:
            return False

        # Check user credentials
        user = get_object_or_404(User, email=username)

        if not user:
            return False
        return True
    else:
        return False
