import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from entity.models import Resource, Interface


# noinspection PyUnresolvedReferences
class EntityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_resource = {
            "port": 80,
            "type": "TCP",
            "notes": "Apache"
        }

        cls.basic_address = {
            "hostname": "localhost",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "resource": [{
                "port": 80,
                "type": "TCP",
                "notes": "Apache"
            }],
            "mac_address": "33:39:34:32:3a:31",
            "mac_vendor": "Extel"
        }

        cls.extended_address = {
            "hostname": "localhost",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "resource": [{
                "port": 80,
                "type": "TCP",
                "notes": "Apache"
            }, {
                "port": 8080,
                "type": "UDP",
                "notes": "video"
            }],
            "mac_address": "33:39:34:32:3a:31",
            "mac_vendor": "Extel"
        }

        cls.basic_entity = {
            "name": "Sky router",
            "notes": "SKY+",
            "type": "DEVICE",
            "hardware": "Sky",
            "interface": [
                {
                    "hostname": "localhost",
                    "ip_v4": "192.168.0.1",
                    "ip_v6": "::1",
                    "resource": [{
                        "port": 80,
                        "type": "TCP",
                        "notes": "Apache"
                    }, {
                        "port": 443,
                        "type": "TCP",
                        "notes": "NGINX"
                    }],
                    "mac_address": "33:39:34:32:3a:31",
                    "mac_vendor": "Extel"
                }
            ],
            "status": "UP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

        cls.bad_uuid = {
            "name": "Sky router",
            "notes": "SKY+",
            "type": "WIFI_AP",
            "hardware": "Sky",
            "interface": [
                {
                    "hostname": "localhost",
                    "ip_v4": "192.168.0.1",
                    "ip_v6": "::1",
                    "resource": [],
                    "mac_address": "1234",
                    "mac_vendor": "Extel"
                }
            ],
            "status": "UP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

        cls.extended_entity = {
            "name": "Rogue Access Point",
            "notes": "Rogue",
            "type": "WIFI_AD_HOC",
            "hardware": "RaspberryPi",
            "interface": [
                {
                    "hostname": "hacked",
                    "ip_v4": "10.0.0.1",
                    "ip_v6": "::ff",
                    "resource": [{
                        "port": 88,
                        "type": "UDP",
                        "notes": "Apache"
                    }, {
                        "port": 443,
                        "type": "TCP",
                        "notes": "NGINX"
                    }],
                    "mac_address": "33:39:34:32:3a:31",
                    "mac_vendor": "Extel"
                },
                {
                    "hostname": "hostname",
                    "ip_v4": "10.0.0.2",
                    "ip_v6": "::2",
                    "resource": [{
                        "port": 80,
                        "type": "TCP",
                        "notes": "Apache"
                    }, {
                        "port": 443,
                        "type": "TCP",
                        "notes": "NGINX"
                    }],
                    "mac_address": "44:49:44:42:4a:41",
                    "mac_vendor": "Antel"
                }
            ],
            "status": "DOWN",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        pass

    def tearDown(self):
        pass

    def test_bad(self):
        response = self.client.post('/api/v1/entities/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_uuid_failure(self):
        uuid_bad = {
            "name": "Sky router",
            "interface": [{
                "mac_address": "1234",
                "resource": []
            }]
        }

        response = self.client.post('/api/v1/entities/', uuid_bad, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['interface'][0].get('mac_address')[0], 'MAC Address must be valid')

    def test_create_resource(self):
        self.create_resource(self.basic_resource)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')
        self.delete_resource(1)

    def test_update_resource(self):
        self.create_resource(self.basic_resource)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

        self.update_resource(resource_id=1, resource={
            "port": 81,
            "type": "UDP",
            "notes": "Apache"
        })
        update = self.get_resource(1)
        self.assertEqual(update.get('port'), 81)
        self.assertEqual(update.get('type'), 'UDP')
        self.assertEqual(update.get('notes'), 'Apache')

        self.delete_resource(1)

    def test_patch_resource(self):
        self.create_resource(self.basic_resource)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

        self.patch_resource(resource_id=1, resource={"notes": 'video'})
        update = self.get_resource(1)
        self.assertEqual(update.get('port'), 80)
        self.assertEqual(update.get('type'), 'TCP')
        self.assertEqual(update.get('notes'), 'video')

        self.patch_resource(resource_id=1, resource={"port": 81})
        update = self.get_resource(1)
        self.assertEqual(update.get('port'), 81)
        self.assertEqual(update.get('type'), 'TCP')
        self.assertEqual(update.get('notes'), 'video')

        self.patch_resource(resource_id=1, resource={"type": 'UDP'})
        update = self.get_resource(1)
        self.assertEqual(update.get('port'), 81)
        self.assertEqual(update.get('type'), 'UDP')
        self.assertEqual(update.get('notes'), 'video')

        self.delete_resource(1)

    def test_create_address(self):
        self.create_address(self.basic_address)
        interface = self.get_interface(1)

        self.assertEqual(interface.get('hostname'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('mac_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('mac_vendor'), 'Extel')

        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')
        self.delete_interface(1)

    def test_update_address(self):
        self.create_address(self.basic_address)
        # Ensure correct number of addresses and resources in the table
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 1)
        self.update_address(resource_id=1, resource=self.extended_address)

        # Ensure correct number of addresses and resources in the table
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 2)

        interface = self.get_interface(1)

        self.assertEqual(interface.get('hostname'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('mac_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('mac_vendor'), 'Extel')

        self.assertEqual(len(interface.get('resource')), 2)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')
        self.delete_interface(1)

    def test_patch_address(self):
        self.create_address(self.basic_address)
        self.patch_address(resource_id=1, resource={
            "hostname": "ultra-host"
        })

        interface = self.get_interface(1)
        self.assertEqual(interface.get('hostname'), 'ultra-host')

        self.patch_address(resource_id=1, resource={
            "resource": [{
                "id": 1,
                "port": 81
            }]
        })

        interface = self.get_interface(1)
        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 81)

        self.patch_address(resource_id=1, resource={
            "ip_v4": "127.0.0.1",
            "ip_v6": "::ff",
            "resource": [{
                "id": "1",
                "notes": "nginx"
            }],
            "mac_address": "00:00:00:00:00:00"
        })
        interface = self.get_interface(1)
        self.assertEqual(interface.get('hostname'), 'ultra-host')
        self.assertEqual(interface.get('ip_v4'), '127.0.0.1')
        self.assertEqual(interface.get('ip_v6'), '::ff')
        self.assertEqual(interface.get('mac_address'), '00:00:00:00:00:00')
        self.assertEqual(interface.get('mac_vendor'), 'Extel')

        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 81)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'nginx')

        self.delete_interface(1)

    def test_create_entity(self):
        self.create_entity(self.basic_entity)
        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), "Sky router")
        self.assertEqual(entity.get('notes'), "SKY+")
        self.assertEqual(entity.get('status'), "UP")
        self.assertEqual(entity.get('type'), "DEVICE")
        self.assertEqual(entity.get('hardware'), "Sky")

        # Ensure the correct number of addresses
        self.assertEqual(len(entity.get('interface')), 1)
        interface = entity.get('interface')[0]
        self.assertEqual(interface.get('hostname'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('mac_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('mac_vendor'), 'Extel')

        resource = interface.get('resource')
        # Ensure the correct number of resources
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0].get('port'), 80)
        self.assertEqual(resource[0].get('type'), "TCP")
        self.assertEqual(resource[0].get('notes'), "Apache")
        self.assertEqual(resource[1].get('port'), 443)
        self.assertEqual(resource[1].get('type'), "TCP")
        self.assertEqual(resource[1].get('notes'), "NGINX")
        self.delete_entity(1)

    # def test_update_entity(self):
    #     self.create_entity(self.basic_entity)
    #     # Make sure we have the correct number of Addresses and Resources
    #     self.assertEqual(Address.objects.all().count(), 1)
    #     self.assertEqual(Resource.objects.all().count(), 2)
    #
    #     self.update_entity(resource_id=1, resource=self.extended_entity)
    #     # Make sure we have the correct number of Addresses and Resources
    #     self.assertEqual(Address.objects.all().count(), 2)
    #     self.assertEqual(Resource.objects.all().count(), 4)
    #     entity = self.get_entity(1)
    #
    #     self.assertEqual(entity.get('name'), "Rogue Access Point")
    #     self.assertEqual(entity.get('notes'), "Rogue")
    #     self.assertEqual(entity.get('status'), "DOWN")
    #     self.assertEqual(entity.get('type'), "Hacker")
    #     self.assertEqual(entity.get('hardware'), "RaspberryPi")
    #
    #     # Ensure the correct number of addresses
    #     self.assertEqual(len(entity.get('address')), 2)
    #
    #     address = entity.get('address')[0]
    #     self.assertEqual(address.get('hostname'), 'hacked')
    #     self.assertEqual(address.get('ip_v4'), '10.0.0.1')
    #     self.assertEqual(address.get('ip_v6'), '::ff')
    #     self.assertEqual(address.get('mac_address'), '33:39:34:32:3a:31')
    #     self.assertEqual(address.get('mac_vendor'), 'Extel')
    #
    #     # Ensure the correct number of resources
    #     self.assertEqual(len(address.get('resource')), 2)
    #     resource = address.get('resource')
    #     self.assertEqual(resource[0].get('port'), 88)
    #     self.assertEqual(resource[0].get('type'), "UDP")
    #     self.assertEqual(resource[0].get('notes'), "Apache")
    #     self.assertEqual(resource[1].get('port'), 443)
    #     self.assertEqual(resource[1].get('type'), "TCP")
    #     self.assertEqual(resource[1].get('notes'), "NGINX")
    #
    #     address = entity.get('address')[1]
    #     self.assertEqual(address.get('hostname'), 'hostname')
    #     self.assertEqual(address.get('ip_v4'), '10.0.0.2')
    #     self.assertEqual(address.get('ip_v6'), '::2')
    #     self.assertEqual(address.get('mac_address'), '44:49:44:42:4a:41')
    #     self.assertEqual(address.get('mac_vendor'), 'Antel')
    #
    #     resource = address.get('resource')
    #     # Ensure the correct number of resources
    #     self.assertEqual(len(address.get('resource')), 2)
    #     self.assertEqual(resource[0].get('port'), 80)
    #     self.assertEqual(resource[0].get('type'), "TCP")
    #     self.assertEqual(resource[0].get('notes'), "Apache")
    #     self.assertEqual(resource[1].get('port'), 443)
    #     self.assertEqual(resource[1].get('type'), "TCP")
    #     self.assertEqual(resource[1].get('notes'), "NGINX")
    #
    #     self.update_entity(resource_id=1, resource=self.basic_entity)
    #     # Make sure we have the correct number of Addresses and Resources
    #     self.assertEqual(Address.objects.all().count(), 1)
    #     self.assertEqual(Resource.objects.all().count(), 2)
    #
    #     self.delete_entity(1)

    def test_merge_entity(self):
        self.create_entity(self.basic_entity)

        self.patch_entity(resource_id=1, resource={
            "name": "modem",
            "hardware": "gibson",
            "interface": [{
                "id": 1,
                "hostname": "server",
            }]
        })

        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), 'modem')
        self.assertEqual(entity.get('hardware'), "gibson")

        # Ensure the correct number of addresses
        self.assertEqual(len(entity.get('interface')), 1)
        interface = entity.get('interface')[0]
        self.assertEqual(interface.get('hostname'), 'server')

        self.patch_entity(resource_id=1, resource={
            "name": "modem",
            "hardware": "gibson",
            "interface": [{
                "id": 1,
                "resource": [{
                    "id": 2,
                    "notes": "VAX"
                }]
            }]
        })

        entity = self.get_entity(1)

        self.delete_entity(1)
        interface = entity.get('interface')[0]
        resource = interface.get('resource')
        # Ensure the correct number of resources
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[1].get('notes'), "VAX")

    # Helper methods

    def create_entity(self, resource):
        return self.post(table='entities', body=resource)

    def get_entity(self, resource_id):
        return self.get(table='entities', pk=resource_id)

    def update_entity(self, resource_id, resource):
        return self.put(table='entities', pk=resource_id, body=resource)

    def patch_entity(self, resource_id, resource):
        return self.patch(table='entities', pk=resource_id, body=resource)

    def delete_entity(self, resource_id):
        return self.delete(table='entities', pk=resource_id)

    def create_resource(self, resource):
        return self.post(table='resources', body=resource)

    def get_interface(self, resource_id):
        return self.get(table='addresses', pk=resource_id)

    def update_address(self, resource_id, resource):
        return self.put(table='addresses', pk=resource_id, body=resource)

    def patch_address(self, resource_id, resource):
        return self.patch(table='addresses', pk=resource_id, body=resource)

    def delete_interface(self, resource_id):
        return self.delete(table='addresses', pk=resource_id)

    def create_address(self, resource):
        return self.post(table='addresses', body=resource)

    def get_resource(self, resource_id):
        return self.get(table='resources', pk=resource_id)

    def update_resource(self, resource_id, resource):
        return self.put(table='resources', pk=resource_id, body=resource)

    def patch_resource(self, resource_id, resource):
        return self.patch(table='resources', pk=resource_id, body=resource)

    def delete_resource(self, resource_id):
        return self.delete(table='resources', pk=resource_id)

    # REST Helper methods

    def get(self, table, pk):
        response = self.client.get('/api/v1/{resource}/1/'.format(resource=table), kwargs={'pk': pk})
        self.assertEqual(response.status_code, 200)
        content = response.content
        model = json.loads(content)
        return model

    def post(self, table, body):
        response = self.client.post('/api/v1/{resource}/'.format(resource=table),
                                    body,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        return response

    def put(self, table, pk, body):
        response = self.client.put('/api/v1/{resource}/{pk}/'.format(resource=table, pk=pk),
                                   body,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return response

    def patch(self, table, pk, body):
        response = self.client.patch('/api/v1/{resource}/{pk}/'.format(resource=table, pk=pk),
                                     body,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return response

    def delete(self, table, pk):
        response = self.client.delete('/api/v1/{resource}/{pk}/'.format(resource=table, pk=pk),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 204)
        return response
