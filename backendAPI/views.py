import requests
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pony.orm as pny

from biomio_backend_SCIM.settings import SCIM_ADDR

from biomio_orm import UserORM, Providers, ProviderUsers, BiomioResourceORM, BiomioPoliciesORM, Profiles, DevicesORM,\
    EnrollmentORM
from serializers import UserSerializer, BiomioResourceSerializer, BiomioServiceProviderSerializer, \
    BiomioPoliciesSerializer, DevicesSerializer, BiomioEnrollmentSerializer
from models import BiomioServiceProvider
from .http import JsonResponse, JsonError
from .decorators import header_required
from django.utils.decorators import method_decorator

from ServiceProviderConfigurationEndpoints.schemas import Schema, SchemaSerializer, scim_schemas
from ServiceProviderConfigurationEndpoints.resourcetypes import ResourceType, ResourceTypeSerializer
from ServiceProviderConfigurationEndpoints.serviceproviderconfig import ServiceProviderConfigSerializer, \
    ServiceProviderConfig, Patch, ChangePassword, ServiceProviderConfigMeta


@api_view(['GET', ])
def api_ServiceProviderConfig(request, format=None):
    serializer = ServiceProviderConfigSerializer(
            ServiceProviderConfig(
                meta=ServiceProviderConfigMeta(resourceType=ServiceProviderConfig, version='v1.0'),
                patch=Patch(False),
                changePassword=ChangePassword(False)
            ),
            context={'request': request}
        )
    return JsonResponse(serializer.data)


@api_view(['GET', ])
def api_resource_types_list(request, format=None):
    response = list()
    for pk in scim_schemas:
        scim_schema = scim_schemas.get(pk)

        response.append(
            ResourceTypeSerializer(
                ResourceType(
                    scim_schema.get('model')
                ),
                context={'request': request}
            ).data
        )
    return JsonResponse(response)


@api_view(['GET', ])
def api_resource_types_detail(request, pk, format=None):
    if SCIM_ADDR % pk in scim_schemas:
        scim_schema = scim_schemas.get(SCIM_ADDR % pk)
        serializer = ResourceTypeSerializer(ResourceType(scim_schema.get('model')), context={'request': request})

        return JsonResponse(serializer.data)
    return JsonError('Wrong Resource Type ID', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
def api_schemas_list(request, format=None):
    response = list()
    for pk in scim_schemas:
        scim_schema = scim_schemas.get(pk)

        response.append(
            SchemaSerializer(
                Schema(
                    scim_schema.get('model'),
                    scim_schema.get('serializer'),
                    scim_schema.get('exclude_fields')
                ),
                context={'request': request}
            ).data
        )
    return JsonResponse(response)


@api_view(['GET', ])
def api_schemas_detail(request, pk, format=None):
    if pk in scim_schemas:
        scim_schema = scim_schemas.get(pk)
        serializer = SchemaSerializer(
                Schema(
                    scim_schema.get('model'),
                    scim_schema.get('serializer'),
                    scim_schema.get('exclude_fields')
                ),
                context={'request': request}
            )
        return JsonResponse(serializer.data)
    return JsonError('Wrong Schema ID', status=status.HTTP_404_NOT_FOUND)


class ApiUsersList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        users = UserORM.instance().all(provider_id)
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return JsonResponse(serializer.data)

    @method_decorator(header_required)
    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()

            ProviderUsers(provider_id=provider_id, user_id=user.id)
            pny.commit()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonError(serializer.errors)


class ApiUsersDetail(APIView):
    def get(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            serializer = UserSerializer(user, context={'request': request})
            return JsonResponse(serializer.data)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(header_required)
    @pny.db_session
    def put(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            data = request.data
            serializer = UserSerializer(user, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonError(serializer.errors)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            result = UserORM.instance().delete(user)
            if result:
                return JsonResponse()
            else:
                return JsonError('Not Found!', status=status.HTTP_409_CONFLICT)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)


class ApiBiomioResourcesList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        web_resources = BiomioResourceORM.instance().all(provider_id)
        serializer = BiomioResourceSerializer(web_resources, context={'request': request}, many=True)
        return JsonResponse(serializer.data)

    @method_decorator(header_required)
    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['providerId'] = provider_id

        serializer = BiomioResourceSerializer(data=data)
        if serializer.is_valid():
            web_resource = serializer.save()
            serializer = BiomioResourceSerializer(web_resource, context={'request': request})
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonError(serializer.errors)


class ApiBiomioResourcesDetail(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            serializer = BiomioResourceSerializer(web_resource, context={'request': request})
            return JsonResponse(serializer.data)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(header_required)
    @pny.db_session
    def put(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            data = request.data

            serializer = BiomioResourceSerializer(web_resource, data=data, partial=True)
            if serializer.is_valid():
                web_resource = serializer.save()
                serializer = BiomioResourceSerializer(web_resource, context={'request': request})
                return JsonResponse(serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JsonError(serializer.errors)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            result = BiomioResourceORM.instance().delete(web_resource)
            if result:
                return JsonResponse()
            else:
                return JsonError('Not Found!', status=status.HTTP_409_CONFLICT)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)


class ApiBiomioServiceProviderList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        web_resources = BiomioResourceORM.instance().all(provider_id)

        serializer = BiomioServiceProviderSerializer(
            BiomioServiceProvider(resources=web_resources),
            context={'request': request}
        )

        return JsonResponse(serializer.data)

    # @pny.db_session
    # def post(self, request, provider_id, format=None):
    #     try:
    #         Providers[provider_id]
    #     except pny.ObjectNotFound:
    #         return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)
    #
    #     data = request.data
    #     data['providerId'] = provider_id
    #
    #     serializer = WebResourceSerializer(data=data)
    #     if serializer.is_valid():
    #         web_resource = serializer.save()
    #
    #         return JsonResponse(WebResourceSerializer(web_resource, context={'request': request}).data, status=status.HTTP_201_CREATED)
    #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBiomioPoliciesList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        policies = BiomioPoliciesORM.instance().all(provider_id)
        serializer = BiomioPoliciesSerializer(policies, context={'request': request}, many=True)
        return JsonResponse(serializer.data)

    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return JsonError('Wrong Provider ID', status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['providerId'] = provider_id

        serializer = BiomioPoliciesSerializer(data=data)
        if serializer.is_valid():
            policies = serializer.save()

            return JsonResponse(
                BiomioPoliciesSerializer(policies, context={'request': request}).data, status=status.HTTP_201_CREATED
            )
        return JsonError(serializer.errors)


class ApiBiomioPoliciesDetail(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            serializer = BiomioPoliciesSerializer(policies, context={'request': request})
            return JsonResponse(serializer.data)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(header_required)
    @pny.db_session
    def put(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            data = request.data

            serializer = BiomioPoliciesSerializer(policies, data=data, partial=True)
            if serializer.is_valid():
                policies = serializer.save()
                return JsonResponse(
                    BiomioPoliciesSerializer(policies, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return JsonError(serializer.errors)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            result = BiomioPoliciesORM.instance().delete(policies)
            if result:
                return JsonResponse()
            else:
                return JsonError('Not Found!', status=status.HTTP_409_CONFLICT)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)


class ApiDevicesList(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        try:
            Profiles[pk]
        except pny.ObjectNotFound:
            return JsonResponse('Wrong User ID', status=status.HTTP_404_NOT_FOUND)

        devices = DevicesORM.instance().all(pk)
        serializer = DevicesSerializer(devices, context={'request': request}, many=True)
        return JsonResponse(serializer.data)

    @pny.db_session
    def post(self, request, pk, format=None):
        try:
            Profiles[pk]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong User ID'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['user'] = pk

        serializer = DevicesSerializer(data=data)
        if serializer.is_valid():
            device = serializer.save()

            return Response(DevicesSerializer(device, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDevicesDetail(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        device = DevicesORM.instance().get(pk)
        if device:
            serializer = DevicesSerializer(device, context={'request': request})
            return JsonResponse(serializer.data)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(header_required)
    @pny.db_session
    def put(self, request, pk, format=None):
        device = DevicesORM.instance().get(pk)
        if device:
            data = request.data

            serializer = DevicesSerializer(device, data=data, partial=True)
            if serializer.is_valid():
                device = serializer.save()
                serializer = DevicesSerializer(device, context={'request': request})

                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonError(serializer.errors)
        else:
            return JsonError('Not Found!', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        device = DevicesORM.instance().get(pk)
        if device:
            result = DevicesORM.instance().delete(device)
            if result:
                return JsonResponse()
            else:
                return JsonError('Not Found!', status=status.HTTP_409_CONFLICT)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)


class ApiBiomioEnrollmentDetail(APIView):
    @pny.db_session
    def get(self, request, device_id, format=None):
        enrollment = EnrollmentORM.instance().get(device_id)
        if enrollment:
            serializer = BiomioEnrollmentSerializer(enrollment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    @pny.db_session
    def post(self, request, device_id, format=None):
        data = request.data
        application = 1 if data.get('verification') else 0

        if not data.get('verification'):
            device = DevicesORM.instance().get(device_id)
            if device.device_token:
                print 'http://gate.biom.io/training?device_id=%s&code=AAAAA' % device.device_token
                # requests.post('http://gate.biom.io/training?device_id=%s&code=AAAAA' % device.device_token)
            else:
                return Response({'errors': 'Device not registered!'}, status=status.HTTP_404_NOT_FOUND)

        enrollment = EnrollmentORM.instance().gen_verification_code(dev_id=device_id, application=application)
        if enrollment:
            serializer = BiomioEnrollmentSerializer(enrollment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)
