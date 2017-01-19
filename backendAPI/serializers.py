from rest_framework import serializers
from models import UserMeta, UserName, User, Email, PhoneNumber, BiomioResourcesMeta, BiomioResource, \
    BiomioPolicies, BiomioPoliciesMeta
from biomio_orm import UserORM, BiomioResourceORM, BiomioPoliciesORM
from biomio_backend_SCIM.settings import SCIM_ADDR


class UserMetaSerializer(serializers.Serializer):
    created = serializers.DateTimeField(required=False, read_only=True)
    lastModified = serializers.DateTimeField(required=False, read_only=True)
    location = serializers.HyperlinkedIdentityField(view_name='scim-users-detail', read_only=True)

    def create(self, validated_data):
        return UserMeta(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class UserNameSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    familyName = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)
    givenName = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)
    middleName = serializers.CharField(max_length=30, required=False, allow_blank=True, allow_null=True)
    honorificPrefix = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    honorificSuffix = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    formatted = serializers.CharField(max_length=128, required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return UserName(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class EmailSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    value = serializers.EmailField()
    primary = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Email(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class PhoneNumberSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    value = serializers.CharField(max_length=16)

    def create(self, validated_data):
        return PhoneNumber(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class BiomioResourceForUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)
    domain = serializers.CharField(max_length=255, read_only=True)


class UserSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    externalId = serializers.CharField(max_length=128, required=False, allow_blank=True, allow_null=True)
    userName = serializers.CharField(max_length=150)
    meta = UserMetaSerializer(required=False, allow_null=True, read_only=True)
    name = UserNameSerializer(required=False, allow_null=True)
    emails = EmailSerializer(required=False, many=True, allow_null=True)
    phoneNumbers = PhoneNumberSerializer(required=False, many=True, allow_null=True)
    resources = BiomioResourceForUserSerializer(required=False, read_only=True, many=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]

    def validate_userName(self, value):
        if self.instance:
            result = UserORM.instance().validate_username(value, self.instance.id)
        else:
            result = UserORM.instance().validate_username(value, None)
        if result:
            # print self.instance.id
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        meta_data = validated_data.pop('meta', None)
        name_data = validated_data.pop('name', None)
        emails_data = validated_data.pop('emails', None)
        phones_data = validated_data.pop('phoneNumbers', None)

        user = User(**validated_data)

        if meta_data:
            user_meta = UserMeta(**meta_data)
        else:
            user_meta = UserMeta()
        user.meta = user_meta
        user_meta.location = user

        if name_data:
            user_name = UserName(**name_data)
            user.name = user_name
            user_name.user = user

        if emails_data:
            user.emails = list()
            for email_data in emails_data:
                email = Email(**email_data)
                email.user = user
                user.emails.append(email)
        if phones_data:
            user.phoneNumbers = list()
            for phone_data in phones_data:
                phone = PhoneNumber(**phone_data)
                phone.user = user
                user.phoneNumbers.append(phone)

        return UserORM.instance().save(user)

    def update(self, instance, validated_data):
        meta_data = validated_data.pop('meta', None)
        name_data = validated_data.pop('name', None)
        emails_data = validated_data.pop('emails', None)
        phones_data = validated_data.pop('phoneNumbers', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        if name_data:
            for key, value in name_data.items():
                setattr(instance.name, key, value)
        else:
            instance.name = False

        if meta_data:
            for key, value in meta_data.items():
                setattr(instance.meta, key, value)

        if emails_data:
            instance.emails = list()
            for email_data in emails_data:
                email = Email(**email_data)
                email.user = instance
                instance.emails.append(email)
        else:
            instance.emails = False

        if phones_data:
            instance.phoneNumbers = list()
            for phone_data in phones_data:
                phone = PhoneNumber(**phone_data)
                phone.user = instance
                instance.phoneNumbers.append(phone)
        else:
            instance.phoneNumbers = False

        return UserORM.instance().save(instance)


class BiomioResourceMetaSerializer(serializers.Serializer):
    created = serializers.DateTimeField(required=False, read_only=True)
    lastModified = serializers.DateTimeField(required=False, read_only=True)
    location = serializers.HyperlinkedIdentityField(view_name='scim-biomio-resources-detail', read_only=True)

    def create(self, validated_data):
        return BiomioResourcesMeta(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class BiomioResourceUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    externalId = serializers.CharField(max_length=128, required=False, allow_blank=True, allow_null=True)
    userName = serializers.CharField(max_length=150)


class BiomioResourceSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()

    id = serializers.IntegerField(read_only=True)
    providerId = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=255, required=True)
    domain = serializers.CharField(max_length=255, required=True)

    meta = BiomioResourceMetaSerializer(read_only=True)
    users = BiomioResourceUserSerializer(many=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]

    def to_representation(self, obj):
        representation = super(BiomioResourceSerializer, self).to_representation(obj)

        representation.pop('providerId')
        return representation

    def create(self, validated_data):
        users_data = validated_data.pop('users', None)

        web_resource = BiomioResource(**validated_data)
        if users_data:
            web_resource.users = list()
            for user_data in users_data:
                if user_data.get('id'):
                    user = UserORM.instance().get(user_data.get('id'))
                    web_resource.users.append(user)

        return BiomioResourceORM.instance().save(web_resource)

    def update(self, instance, validated_data):
        users_data = validated_data.pop('users', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if users_data:
            instance.users = list()
            for user_data in users_data:
                if user_data.get('id'):
                    user = UserORM.instance().get(user_data.get('id'))
                    instance.users.append(user)

        return BiomioResourceORM.instance().save(instance)


class BiomioServiceProviderSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()
    resources = BiomioResourceSerializer(many=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]


class BiomioPoliciesMetaSerializer(serializers.Serializer):
    created = serializers.DateTimeField(required=False, read_only=True)
    lastModified = serializers.DateTimeField(required=False, read_only=True)
    location = serializers.HyperlinkedIdentityField(view_name='scim-biomio-policies-detail', read_only=True)

    def create(self, validated_data):
        return BiomioPoliciesMeta(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance


class BiomioPoliciesSerializer(serializers.Serializer):
    schemas = serializers.SerializerMethodField()

    id = serializers.IntegerField(read_only=True)
    providerId = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=255, required=True)
    body = serializers.CharField(max_length=255, required=False)

    meta = BiomioPoliciesMetaSerializer(read_only=True)

    def get_schemas(self, obj):
        return [SCIM_ADDR % obj.__class__.__name__]

    def create(self, validated_data):
        policies = BiomioPolicies(**validated_data)
        return BiomioPoliciesORM.instance().save(policies)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        return BiomioPoliciesORM.instance().save(instance)
