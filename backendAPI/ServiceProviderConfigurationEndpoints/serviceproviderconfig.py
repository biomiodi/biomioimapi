from biomio_backend_SCIM.settings import SCIM_ADDR
from rest_framework import serializers
from datetime import datetime
from django.core.urlresolvers import reverse


class Patch(object):
    def __init__(self, supported):
        self.supported = supported


class ChangePassword(object):
    def __init__(self, supported):
        self.supported = supported


class ServiceProviderConfigMeta(object):
    def __init__(self, resourceType, version, created=None, lastModified=None):
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.version = version

        self.resourceType = resourceType.__name__


class ServiceProviderConfig(object):
    def __init__(self, patch, changePassword, meta):
        self.patch = patch
        self.changePassword = changePassword
        self.meta = meta


class PatchSerializer(serializers.Serializer):
    supported = serializers.BooleanField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    supported = serializers.BooleanField(required=True)


class ServiceProviderConfigMetaSerializer(serializers.Serializer):
    created = serializers.DateTimeField(required=False, read_only=True)
    lastModified = serializers.DateTimeField(required=False, read_only=True)
    version = serializers.CharField(max_length=255, required=True)
    resourceType = serializers.CharField(max_length=255, required=True)

    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        return reverse('scim-service-provider-config-detail')


class ServiceProviderConfigSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()
    patch = PatchSerializer(required=True)
    changePassword = ChangePasswordSerializer(required=True)
    meta = ServiceProviderConfigMetaSerializer(required=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]