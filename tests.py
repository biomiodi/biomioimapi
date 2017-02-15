# from backendAPI.models import User
# from backendAPI.serializers import UserSerializer
#
# data = {
#     "id": 473,
#     "externalId": "222",
#     "userName": "roman.pidvirnyy4@vakoms.com.ua",
#     "meta": {
#     },
#     "name": {
#         "familyName": "Pidvirnyy",
#         "givenName": "Roman",
#         "middleName": "",
#         "formatted": "Roman Pidvirnyy",
#         "honorificPrefix": "",
#         "honorificSuffix": ""
#     },
#     "emails": [
#       {
#         "value": "roman.pidvirnyy@gmail.com",
#         "primary": True
#       },
#       {
#         "value": "roman.pidvirnyi@gmail.com",
#         "primary": False
#       }
#     ],
#     "phoneNumbers": [
#         {
#             "value": "380637230000"
#         },
#         {
#             "value": "380637230001"
#         },
#         {
#             "value": "380637230003"
#         }
#     ]
# }
#
# user_serializer = UserSerializer(data=data)
# user_serializer.is_valid()
#
# user = user_serializer.save()
#
# from backendAPI.biomio_orm import UserORM
# user_instance = UserORM.instance()
# user_obj = user_instance.save(user)
#
# from backendAPI.biomio_orm import UserNameORM
# user_name_instance = UserNameORM.instance()
# user_name = user_name_instance.get(28)
#
# from backendAPI.biomio_orm import UserMetaORM
# user_meta_instance = UserMetaORM.instance()
# user_meta = user_meta_instance.get(28)


# import Crypto.PublicKey.RSA as RSA
# import python_jwt as jwt
# import datetime
#
# key = RSA.generate(1024)
# private_pem = key.exportKey()
# pub_pem = key.publickey().exportKey()
# private_key = RSA.importKey(private_pem)
# pub_key = RSA.importKey(pub_pem)
#
# payload = {'provider': 'provider_unique_name'}
#
# token = jwt.generate_jwt(payload, private_key, 'RS512', datetime.timedelta(minutes=5))
#
# from backendAPI.biomio_orm import ProviderJWTKeysORM
# ProviderJWTKeysORM.instance().set(16)


import pony.orm as pny
import datetime

# database = pny.Database()
# database.bind(
#         'mysql',
#         host='localhost',
#         user='biomio_admin',
#         passwd='gate',
#         db='biomio_db'
#     )
#
# class Phones(database.Entity):
#     _table_ = 'Phones'
#     profileId = pny.Required('Profiles')
#     phone = pny.Required(str)
#     date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
#
#
# class Profiles(database.Entity):
#     _table_ = 'Profiles'
#     id = pny.PrimaryKey(int, auto=True)
#     name = pny.Required(str, 50, default='test_name', lazy=True)
#     type = pny.Required(str, 50, default='USER', sql_type="enum('ADMIN','USER','PROVIDER','PARTNER')", lazy=True)
#     externalId = pny.Optional(str, 128, nullable=True, lazy=True)
#     creation_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
#     last_login_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True, lazy=True)
#     user_name = pny.Required('UserInfo')
#     emails = pny.Set('Emails')
#     phones = pny.Set('Phones')
#
#
# class Emails(database.Entity):
#     _table_ = 'Emails'
#     profileId = pny.Required('Profiles')
#     email = pny.Required(str)
#     verified = pny.Optional(bool, default=False)
#     primary = pny.Optional(bool, default=False)
#     extention = pny.Optional(bool, default=False)
#     date_created = pny.Optional(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
#
#
# class UserInfo(database.Entity):
#     _table_ = 'UserInfo'
#     id = pny.PrimaryKey(int, auto=True)
#     profileId = pny.Optional('Profiles')
#     firstName = pny.Optional(str, 50, lazy=True, nullable=True)
#     lastName = pny.Optional(str, 50, lazy=True, nullable=True)
#     middleName = pny.Optional(str, 30, lazy=True, nullable=True)
#     honorificPrefix = pny.Optional(str, 10, lazy=True, nullable=True)
#     honorificSuffix = pny.Optional(str, 10, lazy=True, nullable=True)
#     formatted = pny.Optional(str, 128, lazy=True, nullable=True)
#
#     dateCreated = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
#     dateModified = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
#
# database.generate_mapping(create_tables=True)
#
#
# @pny.db_session
# def test():
#     # profile = Profiles(name='test_session')
#     # print profile.id, profile.name
#     #
#     # email = Emails(profileId=profile, email='test_session@mail.com')
#     # print email.id, email.profileId
#     #
#     # email = Emails(profileId=profile, email='test_session1@mail.com')
#     # print email.id, email.profileId
#     #
#     # phone = Phones(profileId=profile, phone='123')
#     # print phone.id, phone.profileId
#     #
#     # phone = Phones(profileId=profile, phone='456')
#     # print phone.id, phone.profileId
#     #
#     # phone = Phones(profileId=profile, phone='789')
#     # print phone.id, phone.profileId
#     #
#     # user_info = UserInfo(firstName='Test')
#     #
#     # pny.commit()
#     # profiles = pny.select(p for p in Profiles if p.name > '')
#     # for p in profiles:
#     #     print p.name
#     #     print p.emails
#     from backendAPI.models import User
#     print User.get(12)
# test()

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from backendAPI.biomio_orm import ProviderJWTKeysORM


data = {
    "externalId": None,
    "userName": "test_user@gmail.com",
    "name": {
        "familyName": "Test",
        "givenName": "Test",
        "middleName": None,
        "honorificPrefix": None,
        "honorificSuffix": None,
        "formatted": None
    },
    "emails": [
        {
            "value": "test_user@gmail.com",
            "primary": True
        }
    ],
    "phoneNumbers": [
        {
            "value": "+12025550165"
        }
    ]
}

provider_id = 16
user_pk = {'pk': 0}


class UserTest(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(16)

    def test_authorization(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.get(reverse('scim-users-list', kwargs={'provider_id': provider_id}), {}, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_create_user_201(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json', data=data, **header)
        user_pk.update({'pk': response.data.get('id')})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_exists_400(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json', data=data, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_exists_error_text(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        self.assertEqual(response.data.get('userName'), ["A user with that username already exists."])

    def test_delete_user(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-users-detail', kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}), format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_email_validation_400(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'emails': [{'primary': True, 'value': 'test_usergmail.com'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json', data=data, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_email_validation_error_text(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'emails': [{'primary': True, 'value': 'test_usergmail.com'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        self.assertEqual(response.data.get('emails'), [{"value": ["Enter a valid email address."]}])

    def test_create_user_username_required_400(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.pop('userName')
        data.update({'emails': [{'primary': True, 'value': 'test_usergmail.com'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_username_required_error_text(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'emails': [{'primary': True, 'value': 'test_usergmail.com'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        self.assertEqual(response.data.get('userName'), ["This field is required."])

    def test_create_user_phone_validation_400(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'userName': 'test_user@gmail.com'})
        data.update({'emails': [{'primary': True, 'value': 'test_user@gmail.com'}]})
        data.update({'phoneNumbers': [{'value': '6546546546546546565465465'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_phone_validation_error_text(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        self.assertEqual(response.data.get('phoneNumbers'), [{"value": ["Ensure this field has no more than 16 characters."]}])