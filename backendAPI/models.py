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

    def to_dict(self):
        return {
            'lastName': self.familyName,
            'firstName': self.givenName,
            'middleName': self.middleName,
            'honorificPrefix': self.honorificPrefix,
            'honorificSuffix': self.honorificSuffix,
            'formatted': self.formatted
        }


class User(object):
    def __init__(self, userName, externalId=None, name=None, meta=None, emails=list(), phoneNumbers=list(), id=None,
                 resources=None):
        self.id = id
        self.externalId = externalId
        self.userName = userName
        self.meta = meta
        self.name = name
        self.emails = emails
        self.phoneNumbers = phoneNumbers
        self.resources = resources

    def to_dict(self):
        return {
            'externalId': self.externalId,
            'name': self.userName
        }


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


class BiomioResourcesMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


class BiomioResource(object):
    def __init__(self, name=None, domain=None, providerId=None, id=None, meta=None, users=None, secret=None, hook=None):
        self.id = id
        self.providerId = providerId
        self.name = name
        self.domain = domain
        self.hook = hook
        self.secret = secret
        self.meta = meta
        self.users = users

    def to_dict(self):
        return {
            'title': self.name,
            'domain': self.domain
        }


class BiomioPolicies(object):
    def __init__(self, title=None, body=None, providerId=None, id=None, meta=None, resources=None):
        self.id = id
        self.providerId = providerId
        self.title = title
        self.body = body
        self.meta = meta
        self.resources = resources

    def to_dict(self):
        return {
            'name': self.title,
            'body': self.body
        }


class BiomioPoliciesMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


class BiomioDevice(object):
    def __init__(self, title=None, body=None, user=None, id=None, meta=None, status=None, device_token=None):
        self.id = id
        self.user = user
        self.title = title
        self.body = body
        self.meta = meta
        self.device_token = device_token


class BiomioDeviceMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location


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


class BiomioEnrollmentVerification(object):
    def __init__(self, code=None, status=None):
        self.code = code
        self.status = status


class BiomioEnrollmentTraining(object):
    def __init__(self, status=None, progress=None, code=None):
        self.status = status
        self.progress = progress
        self.code = code


class BiomioEnrollmentBiometrics(object):
    def __init__(self, type=None, training=None):
        self.type = type
        self.training = training


class BiomioEnrollment(object):
    def __init__(self, biometrics=None, verification=None):
        self.verification = verification
        self.biometrics = biometrics


class Group(object):
    def __init__(self, title=None, body=None, users=None, id=None, meta=None, resources=None, providerId=None):
        self.id = id
        self.providerId = providerId
        self.title = title
        self.body = body
        self.meta = meta
        self.users = users
        self.resources = resources

    def to_dict(self):
        return {
            'title': self.title,
            'body': self.body,
            'providerId': self.providerId
        }


class GroupMeta(object):
    def __init__(self, id=None, pk=None, created=None, lastModified=None, location=None):
        self.id = id
        self.pk = pk
        self.created = created or datetime.now()
        self.lastModified = lastModified or datetime.now()
        self.location = location
