from datetime import datetime


class UserMeta(object):
    def __init__(self, created=None, lastModified=None, location=None, id=None, pk=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


class UserName(object):
    def __init__(self, familyName=None, givenName=None, middleName=None, honorificPrefix=None,
                 honorificSuffix=None, formatted=None, user=None, id=None):
        self.id = id
        self.familyName = familyName
        self.givenName = givenName
        self.middleName = middleName
        self.honorificPrefix = honorificPrefix
        self.honorificSuffix = honorificSuffix
        self.formatted = formatted
        self.user = user


class User(object):
    def __init__(self, userName, externalId=None, name=None, meta=None, emails=None, phoneNumbers=None, id=None,
                 resources=None):
        self.id = id
        self.externalId = externalId
        self.userName = userName
        self.meta = meta
        self.name = name
        self.emails = emails
        self.phoneNumbers = phoneNumbers
        self.resources = resources


class Email(object):
    def __init__(self, value, primary, user=None, id=None):
        self.id = id
        self.user = user
        self.value = value
        self.primary = primary


class PhoneNumber(object):
    def __init__(self, value, user=None, id=None):
        self.id = id
        self.user = user
        self.value = value


class BiomioResource(object):
    def __init__(self, name=None, domain=None, providerId=None, id=None, meta=None, users=None):
        self.id = id
        self.providerId = providerId
        self.name = name
        self.domain = domain
        self.meta = meta
        self.users = users


class BiomioResourcesMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


class BiomioPolicies(object):
    def __init__(self, title=None, body=None, providerId=None, id=None, meta=None, resources=None):
        self.id = id
        self.providerId = providerId
        self.title = title
        self.body = body
        self.meta = meta
        self.resources = resources


class BiomioPoliciesMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


class Device(object):
    def __init__(self, title=None, body=None, profileId=None, id=None, meta=None, status=None, device_token=None):
        self.id = id
        self.user = profileId
        self.title = title
        self.body = body
        self.meta = meta
        self.device_token = device_token


class DeviceMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()


class Application(object):
    def __init__(self, app_type=None, app_id=None):
        self.app_id = app_id
        self.app_type = app_type


class ApplicationsUser(object):
    def __init__(self, user=None, app_id=None):
        self.app_id = app_id
        self.user = user


class BiomioServiceProvider(object):
    def __init__(self, resources=None):
        self.resources = resources