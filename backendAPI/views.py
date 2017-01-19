from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pony.orm as pny

from biomio_backend_SCIM.settings import SCIM_ADDR

from biomio_orm import UserORM, Providers, ProviderUsers, BiomioResourceORM, BiomioPoliciesORM
from serializers import UserSerializer, BiomioResourceSerializer, BiomioServiceProviderSerializer, \
    BiomioPoliciesSerializer
from models import User, BiomioServiceProvider, BiomioPolicies

from ServiceProviderConfigurationEndpoints.schemas import Schema, SchemaSerializer, scim_schemas
from ServiceProviderConfigurationEndpoints.resourcetypes import ResourceType, ResourceTypeSerializer
from ServiceProviderConfigurationEndpoints.serviceproviderconfig import ServiceProviderConfigSerializer, \
    ServiceProviderConfig, Patch, ChangePassword, ServiceProviderConfigMeta


@api_view(['GET', ])
def api_ServiceProviderConfig(request, format=None):
    return Response(
        ServiceProviderConfigSerializer(
            ServiceProviderConfig(
                meta=ServiceProviderConfigMeta(resourceType=ServiceProviderConfig, version='v1.0'),
                patch=Patch(False),
                changePassword=ChangePassword(False)
            ),
            context={'request': request}
        ).data,
        status=status.HTTP_200_OK
    )


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
    return Response(
        response,
        status=status.HTTP_200_OK
    )


@api_view(['GET', ])
def api_resource_types_detail(request, pk, format=None):
    if SCIM_ADDR % pk in scim_schemas:
        scim_schema = scim_schemas.get(SCIM_ADDR % pk)

        return Response(
            ResourceTypeSerializer(
                ResourceType(
                    scim_schema.get('model')
                ),
                context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )
    return Response({'errors': 'Wrong Resource Type ID'}, status=status.HTTP_404_NOT_FOUND)


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
    return Response(
        response,
        status=status.HTTP_200_OK
    )


@api_view(['GET', ])
def api_schemas_detail(request, pk, format=None):
    if pk in scim_schemas:
        scim_schema = scim_schemas.get(pk)

        return Response(
            SchemaSerializer(
                Schema(
                    scim_schema.get('model'),
                    scim_schema.get('serializer'),
                    scim_schema.get('exclude_fields')
                ),
                context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )
    return Response({'errors': 'Wrong Shema ID'}, status=status.HTTP_404_NOT_FOUND)


class ApiUsersList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        users = UserORM.instance().all(provider_id)
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return Response(serializer.data)

    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()

            ProviderUsers(provider_id=provider_id, user_id=user.id)
            pny.commit()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiUsersDetail(APIView):
    def get(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            data = request.data
            serializer = UserSerializer(user, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        user = UserORM.instance().get(pk)
        if user:
            result = UserORM.instance().delete(user)
            if result:
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': 'Not Found!'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)


class ApiBiomioResourcesList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        web_resources = BiomioResourceORM.instance().all(provider_id)
        serializer = BiomioResourceSerializer(web_resources, context={'request': request}, many=True)
        return Response(serializer.data)

    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['providerId'] = provider_id

        serializer = BiomioResourceSerializer(data=data)
        if serializer.is_valid():
            web_resource = serializer.save()

            return Response(BiomioResourceSerializer(web_resource, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBiomioResourcesDetail(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            serializer = BiomioResourceSerializer(web_resource, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    @pny.db_session
    def put(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            data = request.data

            serializer = BiomioResourceSerializer(web_resource, data=data, partial=True)
            if serializer.is_valid():
                web_resource = serializer.save()
                return Response(BiomioResourceSerializer(web_resource, context={'request': request}).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        web_resource = BiomioResourceORM.instance().get(pk)
        if web_resource:
            result = BiomioResourceORM.instance().delete(web_resource)
            if result:
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': 'Not Found!'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)


class ApiBiomioServiceProviderList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        web_resources = BiomioResourceORM.instance().all(provider_id)

        serializer = BiomioServiceProviderSerializer(
            BiomioServiceProvider(resources=web_resources),
            context={'request': request}
        )

        return Response(serializer.data)

    # @pny.db_session
    # def post(self, request, provider_id, format=None):
    #     try:
    #         Providers[provider_id]
    #     except pny.ObjectNotFound:
    #         return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)
    #
    #     data = request.data
    #     data['providerId'] = provider_id
    #
    #     serializer = WebResourceSerializer(data=data)
    #     if serializer.is_valid():
    #         web_resource = serializer.save()
    #
    #         return Response(WebResourceSerializer(web_resource, context={'request': request}).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBiomioPoliciesList(APIView):
    @pny.db_session
    def get(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        policies = BiomioPoliciesORM.instance().all(provider_id)
        serializer = BiomioPoliciesSerializer(policies, context={'request': request}, many=True)
        return Response(serializer.data)

    @pny.db_session
    def post(self, request, provider_id, format=None):
        try:
            Providers[provider_id]
        except pny.ObjectNotFound:
            return Response({'errors': 'Wrong Provider ID'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['providerId'] = provider_id

        serializer = BiomioPoliciesSerializer(data=data)
        if serializer.is_valid():
            policies = serializer.save()

            return Response(
                BiomioPoliciesSerializer(policies, context={'request': request}).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBiomioPoliciesDetail(APIView):
    @pny.db_session
    def get(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            serializer = BiomioPoliciesSerializer(policies, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    @pny.db_session
    def put(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            data = request.data

            serializer = BiomioPoliciesSerializer(policies, data=data, partial=True)
            if serializer.is_valid():
                policies = serializer.save()
                return Response(
                    BiomioPoliciesSerializer(policies, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        policies = BiomioPoliciesORM.instance().get(pk)
        if policies:
            result = BiomioPoliciesORM.instance().delete(policies)
            if result:
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': 'Not Found!'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'errors': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)