import python_jwt as jwt
import Crypto.PublicKey.RSA as RSA

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from biomio_orm import ProviderJWTKeysORM, ProviderUsersORM, BiomioResourceORM, BiomioPoliciesORM, BiomioDevicesORM

from .http import JsonError

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback


def header_required(view_func):
    """Decorator which ensures the header is correct"""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.content_type != 'application/json':
            return JsonError('Content-Type should be an application/json')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def jwt_required(view_func):
    """Decorator which ensures the jwt token is correct"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            return Response(
                {
                    'code': 'authorization_header_missing',
                    'description': 'Authorization header is expected'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return Response(
                {
                    'code': 'invalid_header',
                    'description': 'Authorization header must start with Bearer'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif len(parts) == 1:
            return Response(
                {
                    'code': 'invalid_header',
                    'description': 'Token not found'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif len(parts) > 2:
            return Response(
                {
                    'code': 'invalid_header',
                    'description': 'Authorization header must be Bearer + \s + token'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            provider_id = kwargs.get('provider_id')
        except Exception as e:
            return Response(
                {
                    'code': 'invalid_url',
                    'description': 'Url must contain provider id'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = parts[1]
        private_key = ProviderJWTKeysORM.instance().get(provider_id)

        if private_key:
            private_key = RSA.importKey(private_key)
            try:
                header, claims = jwt.verify_jwt(token, private_key, ['RS256'])
            except jwt._JWTError as err:
                return Response(
                    {
                        'code': 'invalid_token',
                        'description': 'JWT token - %s' % err.message
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except Exception as err:
                return Response(
                    {
                        'code': 'invalid_token',
                        'description': 'JWT token - %s' % err.message
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {
                    'code': 'invalid_token',
                    'description': 'JWT token - invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def provider_user(view_func):
    """Decorator which ensures user related to provider"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not ProviderUsersORM.instance().get(providerId=kwargs.get('provider_id'), userId=kwargs.get('pk')):
            return Response(
                {
                    'code': 'invalid_provider',
                    'description': 'Wrong User or Provider!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def provider_biomio_resource(view_func):
    """Decorator which ensures user related to provider"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        biomio_resource = BiomioResourceORM.instance().get(kwargs.get('pk'))

        if (not biomio_resource) or (int(biomio_resource.providerId) != int(kwargs.get('provider_id'))):
            return Response(
                {
                    'code': 'invalid_provider',
                    'description': 'Wrong Biomio Resource or Provider!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def provider_biomio_policies(view_func):
    """Decorator which ensures user related to provider"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        biomio_policies = BiomioPoliciesORM.instance().get(kwargs.get('pk'))

        if (not biomio_policies) or (int(biomio_policies.providerId) != int(kwargs.get('provider_id'))):
            return Response(
                {
                    'code': 'invalid_provider',
                    'description': 'Wrong Biomio Policies or Provider!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def provider_biomio_device(view_func):
    """Decorator which ensures device related to provider"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            biomio_device = BiomioDevicesORM.instance().get(kwargs.get('pk'))
            if biomio_device and not ProviderUsersORM.instance().get(providerId=kwargs.get('provider_id'), userId=biomio_device.user):
                return Response(
                    {
                        'code': 'invalid_provider',
                        'description': 'Wrong Device or Provider!'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Exception:
            return Response(
                {
                    'code': 'invalid_provider',
                    'description': 'Wrong Device or Provider!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view