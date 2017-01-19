from biomio_backend_SCIM.settings import SCIM_ADDR
from rest_framework import serializers


class ResourceTypeMeta(object):
    def __init__(self, resourceType, pk):
        self.resourceType = resourceType
        self.pk = pk


class ResourceType(object):
    def __init__(self, model):
        self.id = model.__name__
        self.name = self.id
        self.endpoint = '/' + self.id
        self.schema = SCIM_ADDR % self.id

        self.meta = ResourceTypeMeta(self.__class__.__name__, self.id)


class ResourceTypeMetaSerializer(serializers.Serializer):
    resourceType = serializers.CharField(max_length=16, required=True)
    location = serializers.HyperlinkedIdentityField(view_name='scim-resource-type-detail')


class ResourceTypeSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()

    id = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)
    endpoint = serializers.CharField(max_length=255, required=True)
    schema = serializers.CharField(max_length=255, required=True)

    meta = ResourceTypeMetaSerializer(required=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]
