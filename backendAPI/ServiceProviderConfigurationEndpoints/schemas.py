from biomio_backend_SCIM.settings import SCIM_ADDR
from rest_framework import serializers
from backendAPI.models import User, BiomioResource, BiomioServiceProvider, BiomioPolicies
from backendAPI.serializers import UserSerializer, BiomioResourceSerializer, BiomioServiceProviderSerializer, \
    BiomioPoliciesSerializer


scim_types = {
    serializers.IntegerField: 'integer',
    serializers.CharField: 'string',
    serializers.FloatField: 'decimal',
    serializers.BooleanField: 'boolean',
    serializers.DateField: 'dateTime',
    serializers.DateTimeField: 'dateTime'
}


scim_schemas = {
    SCIM_ADDR % 'User': {
        'model': User,
        'serializer': UserSerializer(),
        'exclude_fields': ['schemas']
    },
    SCIM_ADDR % 'BiomioResource': {
        'model': BiomioResource,
        'serializer': BiomioResourceSerializer(),
        'exclude_fields': ['schemas']
    },
    SCIM_ADDR % 'BiomioPolicies': {
        'model': BiomioPolicies,
        'serializer': BiomioPoliciesSerializer(),
        'exclude_fields': ['schemas']
    }
}


class SchemaAttributes(object):
    def __init__(self, name, field):
        self.name = name

        self._type = scim_types[type(field)] if type(field) in scim_types else 'complex'

        self.multiValued = hasattr(field, 'many') and field.many
        self.required = field.required

        self.mutability = 'readOnly' if field.read_only else 'writeOnly' if field.write_only else 'readWrite'
        self.returned = 'always'

        # TODO uniqueness
        self.uniqueness = None

        self.subAttributes = list()

        if isinstance(field, (serializers.Serializer, )):
            for key in field.fields.keys():
                self.subAttributes.append(SchemaAttributes(key, field.fields[key]))
        if isinstance(field, (serializers.ListSerializer,)):
            for key in field.child.fields.keys():
                self.subAttributes.append(SchemaAttributes(key, field.child.fields[key]))


class SchemaMeta(object):
    def __init__(self, resourceType, pk):
        self.resourceType = resourceType
        self.pk = pk


class Schema(object):
    def __init__(self, model, serializer, exclude_fields):
        self.name = model.__name__
        self.id = SCIM_ADDR % self.name

        self.attributes = list()

        # for exclude_field in exclude_fields:
        #     # print exclude_field
        #     serializer.fields.pop(exclude_field)

        for key in serializer.fields.keys():
            if key not in exclude_fields:
                self.attributes.append(SchemaAttributes(key, serializer.fields[key]))

        self.meta = SchemaMeta(self.__class__.__name__, self.id)


class SchemaMetaSerializer(serializers.Serializer):
    resourceType = serializers.CharField(max_length=16, required=True)
    location = serializers.HyperlinkedIdentityField(view_name='scim-schemas-detail')


class SchemaSubAttributesSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255, required=True)
    multiValued = serializers.BooleanField(required=True)
    required = serializers.BooleanField(required=True)
    mutability = serializers.CharField(max_length=10, required=True)
    returned = serializers.CharField(max_length=16, required=True)
    uniqueness = serializers.CharField(max_length=16, required=True)

    def get_type(self, obj):
        return str(obj._type)


class SchemaAttributesSerializer(SchemaSubAttributesSerializer):
    subAttributes = SchemaSubAttributesSerializer(many=True)

    def to_representation(self, obj):
        ret = super(SchemaAttributesSerializer, self).to_representation(obj)

        if not obj.subAttributes:
            ret.pop('subAttributes')
        return ret


class SchemaSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)
    attributes = SchemaAttributesSerializer(many=True)
    meta = SchemaMetaSerializer(required=True)
