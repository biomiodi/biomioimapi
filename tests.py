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


import Crypto.PublicKey.RSA as RSA
import python_jwt as jwt
import datetime

key = RSA.generate(1024)
private_pem = key.exportKey()
pub_pem = key.publickey().exportKey()
private_key = RSA.importKey(private_pem)
pub_key = RSA.importKey(pub_pem)

payload = {'provider': 'provider_unique_name'}

token = jwt.generate_jwt(payload, private_key, 'RS512', datetime.timedelta(minutes=5))

from backendAPI.biomio_orm import ProviderJWTKeysORM
ProviderJWTKeysORM.instance().set(16)