import pony.orm as pny
import datetime
import redis

from backendAPI.models import BiomioResourcesMeta
from models import UserMeta, UserName, User, Email, PhoneNumber, BiomioResource, BiomioPolicies, BiomioPoliciesMeta, \
    Device, DeviceMeta, Application, \
    BiomioEnrollment, BiomioEnrollmentBiometrics, BiomioEnrollmentTraining, BiomioEnrollmentVerification
from biomio_backend_SCIM.settings import DATABASES
import random

REDIS_BIOMIO_GENERAL_CHANNEL = 'biomio_general:%s'
REDIS_TRAINING_STATUS_KEY_PARAMS = REDIS_BIOMIO_GENERAL_CHANNEL % 'params:training:status:%s'

# import warnings
#
#
# warnings.filterwarnings("ignore", "Field 'phones' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'password' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'temp_pass' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'last_ip' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'voice' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'motto' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'bday' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'occupation' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'api_id' doesn't have a default value")
# warnings.filterwarnings("ignore", "Field 'acc_type' doesn't have a default value")


db_parameters = DATABASES.get('default')

database = pny.Database()
database.bind(
        'mysql',
        host=db_parameters.get('HOST'),
        user=db_parameters.get('USER'),
        passwd=db_parameters.get('PASSWORD'),
        db=db_parameters.get('NAME')
    )


class Phones(database.Entity):
    _table_ = 'Phones'
    profileId = pny.Required(int)
    phone = pny.Required(str)
    date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class Emails(database.Entity):
    _table_ = 'Emails'
    profileId = pny.Required(int)
    email = pny.Required(str)
    verified = pny.Optional(bool, default=False)
    primary = pny.Optional(bool, default=False)
    extention = pny.Optional(bool, default=False)
    date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class Profiles(database.Entity):
    _table_ = 'Profiles'
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str, 50, default='test_name', lazy=True)
    type = pny.Required(str, 50, default='USER', sql_type="enum('ADMIN','USER','PROVIDER','PARTNER')", lazy=True)
    externalId = pny.Optional(str, 128, nullable=True, lazy=True)
    creation_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    last_login_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True, lazy=True)


class UserInfo(database.Entity):
    _table_ = 'UserInfo'
    id = pny.PrimaryKey(int, auto=True)
    profileId = pny.Required(int)
    firstName = pny.Optional(str, 50, lazy=True, nullable=True)
    lastName = pny.Optional(str, 50, lazy=True, nullable=True)
    middleName = pny.Optional(str, 30, lazy=True, nullable=True)
    honorificPrefix = pny.Optional(str, 10, lazy=True, nullable=True)
    honorificSuffix = pny.Optional(str, 10, lazy=True, nullable=True)
    formatted = pny.Optional(str, 128, lazy=True, nullable=True)

    dateCreated = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    dateModified = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class Providers(database.Entity):
    _table_ = 'Providers'
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str, 255, lazy=True)


class ProviderUsers(database.Entity):
    _table_ = 'ProviderUsers'
    id = pny.PrimaryKey(int, auto=True)
    provider_id = pny.Required(int)
    user_id = pny.Required(int)


class BiomioResources(database.Entity):
    _table_ = 'WebResources'
    id = pny.PrimaryKey(int, auto=True)
    providerId = pny.Required(int)
    title = pny.Required(str, 255, lazy=True)
    domain = pny.Required(str, 255, lazy=True)
    date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    date_modified = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class BiomioResourceUsers(database.Entity):
    _table_ = 'WebResourceUsers'
    id = pny.PrimaryKey(int, auto=True)
    userId = pny.Required(int)
    webResourceId = pny.Required(int)


class Policies(database.Entity):
    _table_ = 'Policies'
    id = pny.PrimaryKey(int, auto=True)
    owner = pny.Required(int)
    name = pny.Required(str, 255, lazy=True)
    body = pny.Optional(str, 255, lazy=True)
    dateCreated = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    dateModified = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class WebResourcePolicies(database.Entity):
    _table_ = 'WebResourcePolicies'
    id = pny.PrimaryKey(int, auto=True)
    policiesId = pny.Required(int)
    webResourceId = pny.Required(int)


class Devices(database.Entity):
    _table_ = 'UserServices'
    id = pny.PrimaryKey(int, auto=True)
    profileId = pny.Required(int)
    title = pny.Required(str, 255, lazy=True)
    device_token = pny.Optional(str, 255, lazy=True)
    status = pny.Optional(bool, sql_default=False)
    date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    date_modified = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)


class Applications(database.Entity):
    _table_ = 'Applications'
    app_id = pny.PrimaryKey(str, 255)
    app_type = pny.Required(str, 255, lazy=True)


class ApplicationsUser(database.Entity):
    _table_ = 'application_userinformation'
    application = pny.PrimaryKey(str, 255)
    userinformation = pny.Required(int)


class VerificationCodes(database.Entity):
    _table_ = 'VerificationCodes'
    id = pny.PrimaryKey(int, auto=True)
    code = pny.Required(str, 10, lazy=True)
    device_id = pny.Required(int)
    status = pny.Required(int)
    application = pny.Required(int)
    profileId = pny.Required(int)


# pny.sql_debug(True)
database.generate_mapping(create_tables=True)


class EmailORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = EmailORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Emails):
            data.update({'id': obj.id})
            data.update({'value': obj.email})
            data.update({'primary': obj.primary})
        return data

    @pny.db_session
    def get(self, profileId):
        try:
            emails = pny.select(e for e in Emails if e.profileId == profileId)
            if emails:
                data = list()
                for email in emails:
                    data.append(Email(**self.to_dict(email)))
            else:
                raise pny.ObjectNotFound(Emails)
        except pny.ObjectNotFound:
            data = None
        return data


class PhoneNumberORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = PhoneNumberORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Phones):
            data.update({'id': obj.id})
            data.update({'value': obj.phone})
        return data

    @pny.db_session
    def get(self, profileId):
        try:
            phones = pny.select(p for p in Phones if p.profileId == profileId)
            if phones:
                data = list()
                for phone in phones:
                    data.append(PhoneNumber(**self.to_dict(phone)))
            else:
                raise pny.ObjectNotFound(Phones)
        except pny.ObjectNotFound:
            data = None
        return data


class UserMetaORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserMetaORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, UserInfo):
            data.update({'id': obj.id})
            data.update({'pk': obj.profileId})
            data.update({'location': obj.profileId})
            data.update({'created': obj.dateCreated})
            data.update({'lastModified': obj.dateModified})
        return data

    @pny.db_session
    def get(self, profileId):
        try:
            user_meta = UserInfo.get(profileId=profileId)
            if user_meta:
                data = UserMeta(**self.to_dict(user_meta))
            else:
                raise pny.ObjectNotFound(UserInfo)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def all(self):
        user_meta_list = UserInfo.select_by_sql('SELECT ui.id, ui.profileId, ui.dateCreated, ui.dateModified '
                                                'FROM UserInfo ui '
                                                'LEFT JOIN Profiles p ON p.id = ui.profileId ')
        data = list()
        for user_meta in user_meta_list:
            data.append(
                UserMeta(**self.to_dict(user_meta))
            )
        return data


class UserNameORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserNameORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, UserInfo):
            data.update({'id': obj.id})
            data.update({'user': obj.profileId})
            data.update({'familyName': obj.lastName})
            data.update({'givenName': obj.firstName})
            data.update({'middleName': obj.middleName})
            data.update({'honorificPrefix': obj.honorificPrefix})
            data.update({'honorificSuffix': obj.honorificSuffix})
            data.update({'formatted': obj.formatted})
        return data

    @pny.db_session
    def get(self, profileId):
        try:
            user_name = UserInfo.get(profileId=profileId)
            if user_name:
                data = UserName(**self.to_dict(user_name))
            else:
                raise pny.ObjectNotFound(UserInfo)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def all(self):
        user_name_list = UserInfo.select_by_sql('SELECT ui.id, ui.profileId, ui.lastName, ui.firstName, '
                                                'ui.middleName, ui.honorificPrefix, ui.honorificSuffix, '
                                                'ui.formatted '
                                                'FROM UserInfo ui '
                                                'LEFT JOIN Profiles p ON p.id = ui.profileId ')
        data = list()
        for user_name in user_name_list:
            data.append(
                UserName(**self.to_dict(user_name))
            )
        return data


class UserORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = UserORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Profiles):
            data.update({'id': obj.id})
            data.update({'externalId': obj.externalId})
            data.update({'userName': obj.name})
        return data

    @pny.db_session
    def all_by_resource_id(self, resource_id):
        user_list = Profiles.select_by_sql('SELECT u.id, u.name, u.externalId '
                                           'FROM Profiles u '
                                           'LEFT JOIN WebResourceUsers wru ON wru.userId = u.id '
                                           'WHERE u.name is not null and u.name > "" AND '
                                           'wru.webResourceId = %s' % resource_id)

        data_list = list()
        for user in user_list:
            data = User(**self.to_dict(user))
            data.meta = UserMetaORM.instance().get(data.id)
            data.name = UserNameORM.instance().get(data.id)
            data.emails = EmailORM.instance().get(data.id)
            data.phoneNumbers = PhoneNumberORM.instance().get(data.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def all(self, provider_id=None):
        if not provider_id:
            user_list = Profiles.select_by_sql('SELECT u.id, u.name, u.externalId '
                                               'FROM Profiles u '
                                               'WHERE u.name is not null and u.name > "" ')
        else:
            user_list = Profiles.select_by_sql('SELECT u.id, u.name, u.externalId '
                                               'FROM Profiles u '
                                               'LEFT JOIN ProviderUsers pu ON pu.user_id = u.id '
                                               'LEFT JOIN Providers p ON p.id = pu.provider_id '
                                               'WHERE u.name is not null and u.name > "" AND '
                                               'p.id = %s' % provider_id)

        data_list = list()
        for user in user_list:
            data = User(**self.to_dict(user))
            data.meta = UserMetaORM.instance().get(data.id)
            data.name = UserNameORM.instance().get(data.id)
            data.emails = EmailORM.instance().get(data.id)
            data.phoneNumbers = PhoneNumberORM.instance().get(data.id)
            data.resources = BiomioResourceORM.instance().all_by_user_id(data.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def validate_username(self, username, id):
        data = False
        user = Profiles.get(name=username)
        if user:
            data = user.id != id
        return data

    @pny.db_session
    def get(self, profileId):
        try:
            user = Profiles.get(id=profileId)
            if user:
                data = User(**self.to_dict(user))
                data.meta = UserMetaORM.instance().get(data.id)
                data.name = UserNameORM.instance().get(data.id)
                data.emails = EmailORM.instance().get(data.id)
                data.phoneNumbers = PhoneNumberORM.instance().get(data.id)
                data.resources = BiomioResourceORM.instance().all_by_user_id(data.id)
            else:
                raise pny.ObjectNotFound(User)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def delete(self, obj):
        try:
            emails = pny.select(e for e in Emails if e.profileId == obj.id)
            for email in emails:
                email.delete()
                pny.commit()

            phones = pny.select(p for p in Phones if p.profileId == obj.id)
            for phone in phones:
                phone.delete()
                pny.commit()

            user_meta_list = pny.select(m for m in UserInfo if m.profileId == obj.id)
            for user_meta in user_meta_list:
                user_meta.delete()
                pny.commit()

            provider_users = pny.select(
                provider_users for provider_users in ProviderUsers if provider_users.user_id == obj.id)
            print provider_users
            if provider_users:
                provider_users.delete()
                pny.commit()

            user = pny.select(u for u in Profiles if u.id == obj.id)
            if user:
                user.delete()
                pny.commit()
            else:
                raise pny.ObjectNotFound(User)
            return True

        except pny.ObjectNotFound:
            return False

    @pny.db_session
    def save(self, obj):
        if isinstance(obj, User):
            if not obj.id:
                user = Profiles(
                    name=obj.userName
                )
                if obj.externalId:
                    user.externalId = obj.externalId
                pny.commit()

                user_meta = None
                if obj.name:
                    user_meta = UserInfo(
                        profileId=user.id,

                        firstName=obj.name.givenName,
                        lastName=obj.name.familyName,
                        middleName=obj.name.middleName,

                        honorificPrefix=obj.name.honorificPrefix,
                        honorificSuffix=obj.name.honorificSuffix,
                        formatted=obj.name.formatted,

                        dateCreated = obj.meta.created,
                        dateModified = obj.meta.lastModified
                    )
                    pny.commit()
                else:
                    user_meta = UserInfo(
                        profileId=user.id,

                        dateCreated=obj.meta.created,
                        dateModified=obj.meta.lastModified
                    )
                    pny.commit()

                if obj.emails:
                    for email in obj.emails:
                        email_data = Emails(
                            profileId=user.id,

                            email=email.value,
                            primary=email.primary
                        )
                        pny.commit()

                if obj.phoneNumbers:
                    for phone in obj.phoneNumbers:
                        phone_data = Phones(
                            profileId=user.id,

                            phone=phone.value,
                        )
                        pny.commit()

                data = self.get(user.id)
            else:
                try:
                    user = Profiles[obj.id]
                except pny.ObjectNotFound:
                    return False
                if user:

                    user.name = obj.userName
                    user.externalId = obj.externalId

                    user_meta = UserMetaORM.instance().get(obj.id)
                    if user_meta:
                        user_meta = UserInfo.get(profileId=obj.id)
                        if obj.name:
                            user_meta.firstName = obj.name.givenName
                            user_meta.lastName = obj.name.familyName
                            user_meta.middleName = obj.name.middleName

                            user_meta.honorificPrefix = obj.name.honorificPrefix
                            user_meta.honorificSuffix = obj.name.honorificSuffix
                            user_meta.formatted = obj.name.formatted
                        if obj.meta:
                            user_meta.dateCreated = obj.meta.created
                            user_meta.dateModified = obj.meta.lastModified

                    else:
                        user_meta = UserInfo(
                            profileId=user.id,

                            firstName=obj.name.givenName,
                            lastName=obj.name.familyName,
                            middleName=obj.name.middleName,

                            honorificPrefix=obj.name.honorificPrefix,
                            honorificSuffix=obj.name.honorificSuffix,
                            formatted=obj.name.formatted,

                            dateCreated=obj.meta.created,
                            dateModified=obj.meta.lastModified or datetime.datetime.now()
                        )
                    pny.commit()

                    if obj.emails:
                        email_list = list()
                        for email in obj.emails:
                            email_data = Emails.get(email=email.value, profileId=user.id)
                            if email_data:
                                email_data.primary = email.primary
                                pny.commit()
                            else:
                                email_data = Emails(email=email.value, profileId=user.id, primary=email.primary)
                                pny.commit()
                            email_list.append(email.value)
                        if email_list:
                            emails = pny.select(e for e in Emails if e.profileId == obj.id and e.email not in email_list)
                            for email in emails:
                                email.delete()
                                pny.commit()
                    # else:
                    #     emails = pny.select(e for e in Emails if e.profileId == obj.id)
                    #     for email in emails:
                    #         email.delete()
                    #         pny.commit()

                    if obj.phoneNumbers:
                        phone_list = list()
                        for phone in obj.phoneNumbers:
                            phone_data = Phones.get(phone=phone.value, profileId=user.id)
                            if not phone_data:
                                phone_data = Phones(phone=phone.value, profileId=user.id)
                            phone_list.append(phone.value)
                            pny.commit()
                        if phone_list:
                            phones = pny.select(p for p in Phones if p.profileId == obj.id and p.phone not in phone_list)
                            for phone in phones:
                                phone.delete()
                                pny.commit()
                    # else:
                    #     phoneNumbers = pny.select(p for p in Phones if p.profileId == obj.id)
                    #     for phone in phoneNumbers:
                    #         phone.delete()
                    #         pny.commit()

                    data = self.get(user.id)
                else:
                    data = False
        else:
            data = False
        return data


class BiomioResourceMetaORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BiomioResourceMetaORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, BiomioResources):
            data.update({'pk': obj.id})
            data.update({'created': obj.date_created})
            data.update({'lastModified': obj.date_modified})
        return data

    @pny.db_session
    def get(self, id):
        try:
            web_resource = BiomioResources.get(id=id)
            if web_resource:
                data = BiomioResourcesMeta(**self.to_dict(web_resource))
            else:
                raise pny.ObjectNotFound(BiomioResources)
        except pny.ObjectNotFound:
            data = None
        return data


class BiomioResourceORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BiomioResourceORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, BiomioResources):
            data.update({'id': obj.id})
            data.update({'providerId': obj.providerId})
            data.update({'name': obj.title})
            data.update({'domain': obj.domain})
        return data

    @pny.db_session
    def get(self, id):
        try:
            web_resource = BiomioResources.get(id=id)
            if web_resource:
                data = BiomioResource(**self.to_dict(web_resource))
                data.meta = BiomioResourceMetaORM.instance().get(data.id)
                data.users = UserORM.instance().all_by_resource_id(resource_id=id)
            else:
                raise pny.ObjectNotFound(BiomioResources)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def all_by_user_id(self, user_id=None):
        web_resource_list = BiomioResources.select_by_sql('SELECT wr.id, wr.title, wr.domain '
                                                          'FROM WebResources wr '
                                                          'LEFT JOIN WebResourceUsers wru ON wru.webResourceId = wr.id '
                                                          'WHERE wru.userId = %s' % user_id)

        data_list = list()
        for web_resource in web_resource_list:
            data = BiomioResource(**self.to_dict(web_resource))
            data.meta = BiomioResourceMetaORM.instance().get(data.id)
            data.users = UserORM.instance().all_by_resource_id(resource_id=web_resource.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def all_by_policies_id(self, policies_id=None):
        # print web_resource_list
        web_resource_list = BiomioResources.select_by_sql('SELECT wr.id, wr.title, wr.domain '
                                                          'FROM WebResources wr '
                                                          'LEFT JOIN WebResourcePolicies wrp ON wrp.webResourceId = wr.id '
                                                          'WHERE wrp.policiesId = %s' % policies_id)

        data_list = list()
        for web_resource in web_resource_list:
            data = BiomioResource(**self.to_dict(web_resource))
            data.meta = BiomioResourceMetaORM.instance().get(data.id)
            data.users = UserORM.instance().all_by_resource_id(resource_id=web_resource.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def all(self, provider_id=None):
        if not provider_id:
            web_resource_list = BiomioResources.select_by_sql('SELECT wr.id, wr.title, wr.domain '
                                                              'FROM WebResources wr ')
        else:
            web_resource_list = BiomioResources.select_by_sql('SELECT wr.id, wr.title, wr.domain '
                                                              'FROM WebResources wr '
                                                              'WHERE wr.providerId = %s' % provider_id)

        data_list = list()
        for web_resource in web_resource_list:
            data = BiomioResource(**self.to_dict(web_resource))
            data.meta = BiomioResourceMetaORM.instance().get(data.id)
            data.users = UserORM.instance().all_by_resource_id(resource_id=web_resource.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def save(self, obj):
        if isinstance(obj, BiomioResource):
            if not obj.id:
                web_resource = BiomioResources(title=obj.name, domain=obj.domain, providerId=obj.providerId)

                pny.commit()

                if obj.users:
                    for user in obj.users:
                        BiomioResourceUsers(userId=user.id, webResourceId=web_resource.id)
                        pny.commit()

                data = self.get(web_resource.id)
            else:
                try:
                    web_resource = BiomioResources[obj.id]
                except pny.ObjectNotFound:
                    return False

                if web_resource:
                    web_resource.title = obj.name
                    web_resource.domain = obj.domain

                    web_resource.date_modified = datetime.datetime.now()

                    pny.commit()

                    if obj.users:
                        user_list = list()
                        for user in obj.users:
                            web_resource_user_data = BiomioResourceUsers.get(userId=user.id, webResourceId=web_resource.id)
                            if not web_resource_user_data:
                                BiomioResourceUsers(userId=user.id, webResourceId=web_resource.id)
                                pny.commit()

                            user_list.append(user.id)
                        if user_list:
                            users = pny.select(wru for wru in BiomioResourceUsers
                                               if wru.webResourceId == web_resource.id
                                               and wru.userId not in user_list)
                            for user in users:
                                user.delete()
                                pny.commit()
                    else:
                        users = pny.select(wru for wru in BiomioResourceUsers
                                           if wru.webResourceId == web_resource.id)
                        for user in users:
                            user.delete()
                            pny.commit()

                    data = self.get(obj.id)
                else:
                    data = False
        else:
            data = False
        return data

    @pny.db_session
    def delete(self, obj):
        try:
            web_resource = BiomioResources.get(id=obj.id)
            if web_resource:

                users = pny.select(wru for wru in BiomioResourceUsers
                                   if wru.webResourceId == web_resource.id)
                for user in users:
                    user.delete()
                    pny.commit()

                web_resource.delete()
                pny.commit()
            else:
                raise pny.ObjectNotFound(BiomioResources)
        except pny.ObjectNotFound:
            return False
        return True


class BiomioPoliciesMetaORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BiomioPoliciesMetaORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Policies):
            data.update({'pk': obj.id})
            data.update({'created': obj.dateCreated})
            data.update({'lastModified': obj.dateModified})
        return data

    @pny.db_session
    def get(self, id):
        try:
            policies = Policies.get(id=id)
            if policies:
                data = BiomioPoliciesMeta(**self.to_dict(policies))
            else:
                raise pny.ObjectNotFound(Policies)
        except pny.ObjectNotFound:
            data = None
        return data


class BiomioPoliciesORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = BiomioPoliciesORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Policies):
            data.update({'id': obj.id})
            data.update({'providerId': obj.owner})
            data.update({'title': obj.name})
            data.update({'body': obj.body})
        return data

    @pny.db_session
    def get(self, id):
        try:
            policies = Policies.get(id=id)
            if policies:
                data = BiomioPolicies(**self.to_dict(policies))
                data.meta = BiomioPoliciesMetaORM.instance().get(data.id)
                data.resources = BiomioResourceORM.instance().all_by_policies_id(policies_id=id)
            else:
                raise pny.ObjectNotFound(Policies)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def all(self, provider_id=None):
        if not provider_id:
            policies_list = Policies.select_by_sql('SELECT p.id, p.owner, p.name, p.body '
                                                   'FROM Policies p ')
        else:
            policies_list = Policies.select_by_sql('SELECT p.id, p.owner, p.name, p.body '
                                                   'FROM Policies p '
                                                   'WHERE p.owner = %s' % provider_id)

        data_list = list()
        for policies in policies_list:
            data = BiomioPolicies(**self.to_dict(policies))
            data.meta = BiomioPoliciesMetaORM.instance().get(data.id)
            data.resources = BiomioResourceORM.instance().all_by_policies_id(policies_id=policies.id)

            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def save(self, obj):
        if isinstance(obj, BiomioPolicies):
            if not obj.id:
                policies = Policies(name=obj.title, owner=obj.providerId)
                if obj.body:
                    policies.body = obj.body

                pny.commit()

                print obj.resources
                if obj.resources:
                    for resource in obj.resources:
                        WebResourcePolicies(policiesId=policies.id, webResourceId=resource.id)
                        pny.commit()

                data = self.get(policies.id)
            else:
                try:
                    policies = Policies[obj.id]
                except pny.ObjectNotFound:
                    return False

                if policies:
                    policies.name = obj.title
                    policies.body = obj.body

                    policies.dateModified = datetime.datetime.now()

                    pny.commit()

                    if obj.resources:
                        resource_list = list()
                        for resource in obj.resources:
                            web_resource_policies_data = WebResourcePolicies.get(policiesId=policies.id, webResourceId=resource.id)
                            if not web_resource_policies_data:
                                BiomioResourceUsers(policiesId=obj.id, webResourceId=resource.id)
                                pny.commit()

                            resource_list.append(resource.id)
                        if resource_list:
                            resources = pny.select(wrp for wrp in WebResourcePolicies
                                                   if wrp.policiesId == policies.id
                                                   and wrp.webResourceId not in resource_list)
                            for resource in resources:
                                resource.delete()
                                pny.commit()
                    else:
                        resources = pny.select(wrp for wrp in WebResourcePolicies
                                               if wrp.policiesId == policies.id)
                        for resource in resources:
                            resource.delete()
                            pny.commit()

                    data = self.get(obj.id)
                else:
                    data = False
        else:
            data = False
        return data

    @pny.db_session
    def delete(self, obj):
        try:
            policies = Policies.get(id=obj.id)
            if policies:

                resources = pny.select(wrp for wrp in WebResourcePolicies
                                       if wrp.policiesId == policies.id)
                for resource in resources:
                    resource.delete()
                    pny.commit()

                policies.delete()
                pny.commit()
            else:
                raise pny.ObjectNotFound(BiomioResources)
        except pny.ObjectNotFound:
            return False
        return True


class DevicesMetaORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = DevicesMetaORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Devices):
            data.update({'pk': obj.id})
            data.update({'created': obj.date_created})
            data.update({'lastModified': obj.date_modified})
        return data

    @pny.db_session
    def get(self, id):
        try:
            devices = Devices.get(id=id)
            if devices:
                data = DeviceMeta(**self.to_dict(devices))
            else:
                raise pny.ObjectNotFound(Devices)
        except pny.ObjectNotFound:
            data = None
        return data


class DevicesORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = DevicesORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Devices):
            data.update({'id': obj.id})
            data.update({'user': obj.profileId})
            data.update({'title': obj.title})
            data.update({'device_token': obj.device_token})
        return data

    @pny.db_session
    def get(self, id):
        try:
            device = Devices.get(id=id)
            if device:
                data = Device(**self.to_dict(device))
                data.meta = DevicesMetaORM.instance().get(data.id)
                if data.device_token:
                    data.application = ApplicationsORM.instance().get(data.device_token)
                else:
                    data.application = None
            else:
                raise pny.ObjectNotFound(Devices)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def all(self, profileId=None):
        devices = pny.select(e for e in Devices if e.profileId == profileId)

        data_list = list()
        for device in devices:
            data = DevicesORM.instance().get(device.id)
            data_list.append(
                data
            )
        return data_list

    @pny.db_session
    def save(self, obj):
        if isinstance(obj, Device):
            if not obj.id:
                device = Devices(title=obj.title, profileId=obj.user)
                pny.commit()

                data = self.get(device.id)
            else:
                try:
                    device = Devices[obj.id]
                except pny.ObjectNotFound:
                    return False

                if device:
                    device.title = obj.title
                    device.date_modified = datetime.datetime.now()

                    pny.commit()

                    data = self.get(obj.id)
                else:
                    data = False
        else:
            data = False
        return data

    @pny.db_session
    def delete(self, obj):
        try:
            #ToDo check necessity of deleting ApplicationsUser and Applications if Device is deleted
            device = Devices[obj.id]
            if device:

                if device.device_token:
                    applications_user = ApplicationsUser[device.device_token]
                    applications_user.delete()
                if device.device_token:
                    application = Applications[device.device_token]
                    application.delete()

                device.delete()

                pny.commit()
            else:
                raise pny.ObjectNotFound(Devices)
        except pny.ObjectNotFound:
            return False
        return True


class ApplicationsORM:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ApplicationsORM()
        return cls._instance

    def to_dict(self, obj):
        data = dict()
        if isinstance(obj, Applications):
            data.update({'app_id': obj.app_id})
            data.update({'app_type': obj.app_type})
        return data

    @pny.db_session
    def get(self, app_id):
        try:
            app = Applications.get(app_id=app_id)
            if app:
                data = Application(**self.to_dict(app))
            else:
                raise pny.ObjectNotFound(Applications)
        except pny.ObjectNotFound:
            data = None
        return data


class EnrollmentORM:
    _instance = None

    STATUS_ARRAY = {
        0: 'non-verified',
        1: 'non-verified',
        2: 'non-verified',
        3: 'verified',
        4: 'in-process',
        5: 'canceled',
        6: 'failed',
        7: 'failed',
        8: 'retry',

    }

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = EnrollmentORM()
        return cls._instance

    @pny.db_session
    def get(self, dev_id):
        try:
            device = Devices.get(id=dev_id)
            if device:
                verification_code = VerificationCodes.get(device_id=dev_id, application=1)
                if verification_code:
                    code = verification_code.code
                    status = verification_code.status
                else:
                    code = None
                    status= False

                enrollment_verification = BiomioEnrollmentVerification(code=code, status=self.STATUS_ARRAY.get(status))

                biometrics = list()
                # device_training = BiomioEnrollmentTraining(status='in-progress', progress='80')

                verification_code = VerificationCodes.get(device_id=dev_id, application=0)
                if verification_code:
                    code = verification_code.code
                    status = verification_code.status
                else:
                    code = None
                    status= False

                pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
                r = redis.Redis(connection_pool=pool)
                # print r.get(REDIS_TRAINING_STATUS_KEY_PARAMS % device.device_token)
                if r.get(REDIS_TRAINING_STATUS_KEY_PARAMS % device.device_token):
                    import ast

                    data = ast.literal_eval(r.get(REDIS_TRAINING_STATUS_KEY_PARAMS % device.device_token))
                    device_training = BiomioEnrollmentTraining(status=data.get('status'), progress=data.get('progress'))
                    device_biometrics = BiomioEnrollmentBiometrics(training=device_training, type='face')
                    biometrics.append(device_biometrics)
                else:
                    device_training = BiomioEnrollmentTraining(status=self.STATUS_ARRAY.get(status), progress=False)
                    device_biometrics = BiomioEnrollmentBiometrics(training=device_training, type='face')
                    biometrics.append(device_biometrics)

                enrollment = BiomioEnrollment(verification=enrollment_verification, biometrics=biometrics)
                data = enrollment
            else:
                raise pny.ObjectNotFound(Devices)
        except pny.ObjectNotFound:
            data = None
        return data

    @pny.db_session
    def gen_verification_code(self, dev_id, application):
        try:
            device = Devices.get(id=dev_id)
            if device:
                verification_code = VerificationCodes.select_by_sql('SELECT v.id, v.code, v.status '
                                                                    'FROM VerificationCodes v '
                                                                    'WHERE v.device_id = "%s" '
                                                                    'AND v.application = %s '
                                                                    'LIMIT 1' % (dev_id, application))
                if verification_code:
                    verification_code = verification_code[0]
                    while True:
                        code = random.randint(10000000, 99999999)
                        if VerificationCodes.select_by_sql('SELECT v.id, v.code, v.status '
                                                           'FROM VerificationCodes v '
                                                           'WHERE v.code = "%s"' % code):
                            continue
                        else:
                            verification_code.code = str(code)
                            verification_code.status = 0
                            verification_code.application = application
                            pny.commit()
                            break
                else:
                    while True:
                        code = random.randint(10000000, 99999999)
                        if VerificationCodes.select_by_sql('SELECT v.id, v.code, v.status '
                                                           'FROM VerificationCodes v '
                                                           'WHERE v.code = "%s"' % code):
                            continue
                        else:
                            verification_code = VerificationCodes(
                                code=str(code),
                                status=0,
                                device_id=dev_id,
                                application=application,
                                profileId=device.profileId
                            )
                            pny.commit()
                            break

                enrollment_verification = BiomioEnrollmentVerification(
                    code=verification_code.code,
                    status=self.STATUS_ARRAY.get(verification_code.status)
                )

                biometrics = list()
                device_training = BiomioEnrollmentTraining(status=self.STATUS_ARRAY.get(verification_code.status), progress=None)
                device_biometrics = BiomioEnrollmentBiometrics(training=device_training, type='face')
                biometrics.append(device_biometrics)

                enrollment = BiomioEnrollment(verification=enrollment_verification, biometrics=biometrics)

                data = enrollment
            else:
                raise pny.ObjectNotFound(Devices)
        except pny.ObjectNotFound:
            data = None
        return data
