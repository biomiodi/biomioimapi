import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from backendAPI.biomio_orm import ProviderJWTKeysORM


data = dict()

provider_id = 16
user_pk = {'pk': 0}
resource_pk = {'pk': 0}
policies_pk = {'pk': 0}
devices_pk = {'pk': 0}
groups_pk = {'pk': 0}


class Test_01_User(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(provider_id)

    def test_001_authorization(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.get(reverse('scim-users-list', kwargs={'provider_id': provider_id}), {}, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_002_create_user_username_required_400(self):
        print '002'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_003_create_user_email_validation_400(self):
        print '003'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'userName': 'TestDev'})
        data.update({'emails': [{'primary': True, 'value': 'TestDevgmail.com'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_004_create_user_phone_validation_400(self):
        print '004'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'emails': [{'primary': True, 'value': 'TestDev@gmail.com'}]})
        data.update({'phoneNumbers': [{'value': '6546546546546546565465465'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_005_create_user_201(self):
        print '005'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'phoneNumbers': [{'value': '380998883355'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk': response.data.get('id')})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_006_create_user_exists_400(self):
        print '006'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'phoneNumbers': [{'value': '380998883355'}]})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json', data=data, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_007_update_user_username_201(self):
        print '007'
        header = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

        data.clear()
        data.update({'userName': 'TestDev1'})

        response = self.client.put(reverse('scim-users-detail',
                                           kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                   format='json',
                                   data=data,
                                   **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('userName'), 'TestDev1')

    def test_008_update_user_emails_add_201(self):
        print '008'
        header = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

        data.clear()
        emails =\
            {
                'emails': [
                    {
                        'primary': True,
                        'value': 'TestDev@gmail.com'
                    },
                    {
                        'primary': False,
                        'value': 'TestDev1@gmail.com'
                    }
                ]
            }
        data.update(emails)

        response = self.client.put(reverse('scim-users-detail',
                                           kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                   format='json',
                                   data=data,
                                   **header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.dumps(response.data.get('emails'), sort_keys=True),
                         json.dumps(emails.get('emails'), sort_keys=True))

    def test_009_update_user_emails_delete_201(self):
        print '009'
        header = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

        data.clear()
        emails = {
            'emails': []
        }
        data.update(emails)

        response = self.client.put(reverse('scim-users-detail',
                                           kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                   format='json',
                                   data=data,
                                   **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('emails'), list())

    def test_010_user_get_200(self):
        print '010'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-users-detail',
                                           kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_011_delete_user(self):
        print '011'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_012_user_get_nonexistent(self):
        print '012'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-users-detail',
                                           kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_02_BiomioResource(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(provider_id)

    def test_013_authorization(self):
        print '013'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.get(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}), {}, **header
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_014_create_biomioresource_required_fields_400(self):
        print '014'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('domain')[0], "This field is required.")
        self.assertEqual(response.data.get('name')[0], "This field is required.")
        # self.assertEqual(response.data.get('users')[0], "This field is required.")

    def test_015_create_biomioresource_201(self):
        print '015'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.update({'userName': 'TestDev_02'})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk': response.data.get('id')})

        data.update({'userName': 'TestDev_03'})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk1': response.data.get('id')})

        data.clear()
        data.update({'users': [{'id': user_pk.get('pk')}, {'id': user_pk.get('pk1')}]})
        data.update({'domain': 'testdev.com'})
        data.update({'name': 'testdev.com'})

        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        resource_pk.update({'pk': response.data.get('id')})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_016_update_biomioresource_201(self):
        print '016'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'users': [{'id': user_pk.get('pk')}]})
        data.update({'domain': 'testdev1.com'})
        data.update({'name': 'testdev1.com'})

        response = self.client.put(
            reverse('scim-biomio-resources-detail', kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('domain'), 'testdev1.com')
        self.assertEqual(response.data.get('name'), 'testdev1.com')

        self.assertEqual(
            json.dumps(response.data.get('users'), sort_keys=True),
            json.dumps([{'id': user_pk.get('pk'), 'externalId': None, 'userName': 'TestDev_02'}], sort_keys=True)
        )

    def test_017_update_biomioresource_201(self):
        print '017'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'users': []})
        data.update({'domain': 'testdev.com'})
        data.update({'name': 'testdev.com'})

        response = self.client.put(
            reverse('scim-biomio-resources-detail', kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('domain'), 'testdev.com')
        self.assertEqual(response.data.get('name'), 'testdev.com')

        self.assertEqual(
            json.dumps(response.data.get('users'), sort_keys=True),
            json.dumps(list(), sort_keys=True)
        )

    def test_018_resource_get_200(self):
        print '018'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-biomio-resources-detail',
                                           kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_019_delete_resource(self):
        print '019'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-biomio-resources-detail',
                                              kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_020_delete_users(self):
        print '020'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk1')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_020_resource_get_nonexistent(self):
        print '021'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-biomio-resources-detail',
                                           kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_03_BiomioPolicies(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(provider_id)

    def test_001_authorization(self):
        print '001 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.get(
            reverse('scim-biomio-policies-list', kwargs={'provider_id': provider_id}), {}, **header
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_002_create_biomiopolicies_required_fields_400(self):
        print '002 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        response = self.client.post(
            reverse('scim-biomio-policies-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('errors')[0].get('title'), "This field is required.")

    def test_003_create_biomiopolicies_201(self):
        print '003 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'title': 'policies-001'})

        response = self.client.post(
            reverse('scim-biomio-policies-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )
        policies_pk.update({'pk': response.data.get('id')})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_004_update_biomiopolicies_201(self):
        print '004 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'domain': 'testdev.com'})
        data.update({'name': 'testdev.com'})

        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        resource_pk.update({'pk': response.data.get('id')})

        data.clear()
        data.update({'domain': 'testdev1.com'})
        data.update({'name': 'testdev1.com'})

        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        resource_pk.update({'pk1': response.data.get('id')})

        data.clear()
        data.update({'title': 'policies-002'})
        data.update({'resources': [{'id': resource_pk.get('pk')}, {'id': resource_pk.get('pk1')}]})

        response = self.client.put(
            reverse('scim-biomio-policies-detail', kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'policies-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk'), "name": "testdev.com"},
                    {"domain": "testdev1.com", "id": resource_pk.get('pk1'), "name": "testdev1.com"}
                ], sort_keys=True)
        )

    def test_005_update_biomiopolicies_201(self):
        print '005 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'resources': [{'id': resource_pk.get('pk')}]})

        response = self.client.put(
            reverse('scim-biomio-policies-detail', kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'policies-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk'), "name": "testdev.com"}
                ], sort_keys=True)
        )

    def test_006_update_biomiopolicies_201(self):
        print '006 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'resources': []})

        response = self.client.put(
            reverse('scim-biomio-policies-detail', kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'policies-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(list(), sort_keys=True)
        )

    def test_007_biomiopolicies_get_200(self):
        print '007 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-biomio-policies-detail',
                                           kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_008_delete_policies(self):
        print '008 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-biomio-policies-detail',
                                              kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_009_delete_resources(self):
        print '009 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-biomio-resources-detail',
                                              kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('scim-biomio-resources-detail',
                                              kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk1')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_010_biomiopolicies_get_nonexistent(self):
        print '010 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-biomio-policies-detail',
                                           kwargs={'provider_id': provider_id, 'pk': policies_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_04_BiomioDevices(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(provider_id)

    def test_001_authorization(self):
        print '001 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'userName': 'TestDev'})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk': response.data.get('id')})

        response = self.client.get(
            reverse('scim-user-biomio-devices-list', kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}), {}, **header
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_002_create_biomiodevices_required_fields_400(self):
        print '002 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        response = self.client.post(
            reverse('scim-user-biomio-devices-list', kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('title')[0], "This field is required.")

    def test_003_create_biomiodevices_201(self):
        print '003 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'title': 'device-001'})
        response = self.client.post(
            reverse('scim-user-biomio-devices-list', kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )
        devices_pk.update({'pk': response.data.get('id')})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'device-001')

    def test_003_update_biomiodevices_201(self):
        print '003 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'title': 'device-002'})
        response = self.client.put(
            reverse('scim-user-biomio-device-detail', kwargs={'provider_id': provider_id, 'pk': devices_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'device-002')

    def test_004_biomiodevices_get_200(self):
        print '004 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(
            reverse('scim-user-biomio-device-detail', kwargs={'provider_id': provider_id, 'pk': devices_pk.get('pk')}),
            **header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_005_delete_biomiodevices(self):
        print '005 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(
            reverse('scim-user-biomio-device-detail', kwargs={'provider_id': provider_id, 'pk': devices_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_006_delete_users(self):
        print '006 devices'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_010_biomiodevices_get_nonexistent(self):
        print '010 policies'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(
            reverse('scim-users-detail', kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_05_Groups(APITestCase):
    def setUp(self):
        self.token = ProviderJWTKeysORM.instance().get_token(provider_id)

    def test_001_authorization(self):
        print '001 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
        response = self.client.get(
            reverse('scim-groups-list', kwargs={'provider_id': provider_id}), {}, **header
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "REST jwt-auth failed")

    def test_002_create_groups_required_fields_400(self):
        print '002 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        response = self.client.post(
            reverse('scim-groups-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('errors')[0].get('title'), "This field is required.")

    def test_003_create_groups_201(self):
        print '003 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'title': 'TestGroupDev-001'})
        response = self.client.post(
            reverse('scim-groups-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )
        groups_pk.update({'pk': response.data.get('id')})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_004_update_groups_201(self):
        print '004 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'title': 'TestGroupDev-002'})
        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

    def test_005_update_groups_201(self):
        print '005 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'domain': 'testdev.com'})
        data.update({'name': 'testdev.com'})

        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        resource_pk.update({'pk': response.data.get('id')})

        data.clear()
        data.update({'domain': 'testdev1.com'})
        data.update({'name': 'testdev1.com'})

        response = self.client.post(
            reverse('scim-biomio-resources-list', kwargs={'provider_id': provider_id}),
            format='json',
            data=data,
            **header
        )

        resource_pk.update({'pk1': response.data.get('id')})

        data.clear()
        data.update({'resources': [{'id': resource_pk.get('pk')}, {'id': resource_pk.get('pk1')}]})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk')},
                    {"domain": "testdev1.com", "id": resource_pk.get('pk1')}
                ], sort_keys=True)
        )

    def test_006_update_groups_201(self):
        print '006 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'userName': 'TestDev_02'})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk': response.data.get('id')})

        data.update({'userName': 'TestDev_03'})
        response = self.client.post(reverse('scim-users-list', kwargs={'provider_id': provider_id}), format='json',
                                    data=data, **header)

        user_pk.update({'pk1': response.data.get('id')})

        data.clear()
        data.update({'users': [{'id': user_pk.get('pk')}, {'id': user_pk.get('pk1')}]})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk')},
                    {"domain": "testdev1.com", "id": resource_pk.get('pk1')}
                ], sort_keys=True)
        )

        self.assertEqual(
            json.dumps(response.data.get('users'), sort_keys=True),
            json.dumps(
                [
                    {"name": "TestDev_02", "id": user_pk.get('pk'), "type": "USER"},
                    {"name": "TestDev_03", "id": user_pk.get('pk1'), "type": "USER"}
                ], sort_keys=True)
        )

    def test_007_update_groups_201(self):
        print '007 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'resources': [{'id': resource_pk.get('pk')}]})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk')}
                ], sort_keys=True)
        )

    def test_008_update_groups_201(self):
        print '008 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'users': [{'id': user_pk.get('pk')}]})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(
                [
                    {"domain": "testdev.com", "id": resource_pk.get('pk')}
                ], sort_keys=True)
        )

        self.assertEqual(
            json.dumps(response.data.get('users'), sort_keys=True),
            json.dumps(
                [
                    {"name": "TestDev_02", "id": user_pk.get('pk'), "type": "USER"}
                ], sort_keys=True)
        )

    def test_009_update_groups_201(self):
        print '009 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'resources': []})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(list(), sort_keys=True))

    def test_010_update_groups_201(self):
        print '010 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        data.clear()
        data.update({'users': []})

        response = self.client.put(
            reverse('scim-groups-detail', kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
            format='json',
            data=data,
            **header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), 'TestGroupDev-002')

        self.assertEqual(
            json.dumps(response.data.get('resources'), sort_keys=True),
            json.dumps(list(), sort_keys=True)
        )

        self.assertEqual(
            json.dumps(response.data.get('users'), sort_keys=True),
            json.dumps(list(), sort_keys=True)
        )

    def test_011_groups_get_200(self):
        print '011 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-groups-detail',
                                              kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_012_delete_groups(self):
        print '012 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-groups-detail',
                                              kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_013_delete_resources(self):
        print '013 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-biomio-resources-detail',
                                              kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('scim-biomio-resources-detail',
                                              kwargs={'provider_id': provider_id, 'pk': resource_pk.get('pk1')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_014_delete_users(self):
        print '014 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('scim-users-detail',
                                              kwargs={'provider_id': provider_id, 'pk': user_pk.get('pk1')}),
                                      format='json', data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_015_groups_get_nonexistent(self):
        print '015 groups'
        header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}

        response = self.client.get(reverse('scim-groups-detail',
                                              kwargs={'provider_id': provider_id, 'pk': groups_pk.get('pk')}), **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
