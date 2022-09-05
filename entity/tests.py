import json
from deepdiff import DeepDiff
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
            "type": "Server",
            "hardware": "Intel",
            "name": "localhost",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "physical_address": "33:39:34:32:3a:31",
            "vendor": "Extel",
            "notes": "local",
            "resource": [{
                "port": 80,
                "type": "TCP",
                "notes": "Apache"
            }],
        }

        cls.extended_address = {
            "type": "Client",
            "hardware": "Intel",
            "name": "localhost",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "physical_address": "33:39:34:32:3a:31",
            "vendor": "Extel",
            "notes": "Local",
            "resource": [{
                "port": 80,
                "type": "TCP",
                "notes": "Apache"
            }, {
                "port": 8080,
                "type": "UDP",
                "notes": "video"
            }],

        }

        cls.basic_entity = {
            "name": "Sky router",
            "notes": "SKY+",
            "type": "Server",
            "hardware": "Sky",
            "interface": [
                {
                    "name": "localhost",
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
                    "physical_address": "33:39:34:32:3a:31",
                    "vendor": "Extel"
                }
            ],
            "status": "UP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

        cls.basic_ssid = {
            "type": "WIFI_AP",
            "hardware": "Sky",
            "name": "Base Station",
            "channel": 10,
            "frequency": 10,
            "crypto": "WPA",
            "BSSID": "33:39:34:32:3a:31",
            "notes": "Rogue AP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387",
            "client": [{
                "type": "Server",
                "name": "localhost",
                "ip_v4": "192.168.0.1",
                "ip_v6": "::1",
                "resource": [{
                    "port": 80,
                    "type": "TCP",
                    "notes": "Apache"
                }]
            }]
        }

        cls.extended_ssid = {
            "type": "WIFI_AP",
            "hardware": "Sky",
            "name": "Base Station",
            "channel": 10,
            "frequency": 10,
            "crypto": "WPA",
            "BSSID": "33:39:34:32:3a:31",
            "notes": "Rogue AP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387",
            "client": [{
                "type": "Server",
                "name": "localhost",
                "ip_v4": "192.168.0.1",
                "ip_v6": "::1",
                "resource": [{
                    "port": 80,
                    "type": "TCP",
                    "notes": "Apache"
                }]
            }, {
                "type": "Client",
                "name": "localhost",
                "ip_v4": "192.168.0.2",
                "ip_v6": "::2",
                "resource": [{
                    "port": 80,
                    "type": "TCP",
                    "notes": "Apache"
                }]
            }]
        }

        cls.bad_uuid = {
            "name": "Sky router",
            "notes": "SKY+",
            "type": "Server",
            "hardware": "Sky",
            "interface": [
                {
                    "name": "localhost",
                    "ip_v4": "192.168.0.1",
                    "ip_v6": "::1",
                    "resource": [],
                    "physical_address": "1234",
                    "vendor": "Extel"
                }
            ],
            "status": "UP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

        cls.extended_entity = {
            "name": "Rogue Access Point",
            "notes": "Rogue",
            "type": "Server",
            "hardware": "RaspberryPi",
            "interface": [
                {
                    "name": "hacked",
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
                    "physical_address": "33:39:34:32:3a:31",
                    "vendor": "Extel"
                },
                {
                    "name": "hostname",
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
                    "physical_address": "44:49:44:42:4a:41",
                    "vendor": "Antel"
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
        self.delete_resource(1, True)
        self.delete_interface(1, True)
        self.delete_entity(1, True)
        self.delete_SSID(1, True)
        pass

    def test_bad(self):
        response = self.client.post('/api/v1/entities/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_uuid_failure(self):
        uuid_bad = {
            "name": "Sky router",
            "interface": [{
                "physical_address": "1234",
                "resource": []
            }]
        }

        response = self.client.post('/api/v1/entities/', uuid_bad, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['interface'][0].get('physical_address')[0], 'MAC Address must be valid')

    def test_create_resource(self):
        self.create_resource(self.basic_resource)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

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

    def test_create_address(self):
        self.create_interface(self.basic_address)
        interface = self.get_interface(1)

        self.assertEqual(interface.get('name'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('vendor'), 'Extel')
        self.assertEqual(interface.get('type'), 'Server')
        self.assertEqual(interface.get('notes'), 'local')

        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

    def test_create_address_basic(self):
        body = {
            "name": "small",
            "ip_v4": "255.255.255.255"
        }

        self.create_interface(body)
        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'small')
        self.assertEqual(interface.get('ip_v4'), '255.255.255.255')
        self.assertEqual(interface.get('resource'), [])

    def test_update_address(self):
        self.create_interface(self.basic_address)
        # Ensure correct number of addresses and resources in the table
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 1)
        self.update_interface(resource_id=1, resource=self.extended_address)

        # Ensure correct number of addresses and resources in the table
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 2)

        interface = self.get_interface(1)

        self.assertEqual(interface.get('name'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('vendor'), 'Extel')

        self.assertEqual(len(interface.get('resource')), 2)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

    def test_patch_address(self):
        self.create_interface(self.basic_address)
        self.patch_interface(resource_id=1, resource={
            "name": "ultra-host"
        })

        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'ultra-host')

        self.patch_interface(resource_id=1, resource={
            "resource": [{
                "id": 1,
                "port": 81
            }]
        })

        interface = self.get_interface(1)
        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 81)

        self.patch_interface(resource_id=1, resource={
            "ip_v4": "127.0.0.1",
            "ip_v6": "::ff",
            "resource": [{
                "id": "1",
                "notes": "nginx"
            }],
            "physical_address": "00:00:00:00:00:00"
        })
        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'ultra-host')
        self.assertEqual(interface.get('ip_v4'), '127.0.0.1')
        self.assertEqual(interface.get('ip_v6'), '::ff')
        self.assertEqual(interface.get('physical_address'), '00:00:00:00:00:00')
        self.assertEqual(interface.get('vendor'), 'Extel')

        self.assertEqual(len(interface.get('resource')), 1)
        resource = interface.get('resource')[0]
        self.assertEqual(resource.get('port'), 81)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'nginx')

    def test_create_ssid(self):
        self.create_SSID(self.basic_ssid)

        ssid = self.get_SSID(1)
        self.assertEqual(ssid.get('type'), "WIFI_AP")
        self.assertEqual(ssid.get('hardware'), "Sky")
        self.assertEqual(ssid.get('name'), "Base Station")
        self.assertEqual(ssid.get('channel'), 10)
        self.assertEqual(ssid.get('frequency'), 10)
        self.assertEqual(ssid.get('crypto'), "WPA")
        self.assertEqual(ssid.get('BSSID'), "33:39:34:32:3a:31")
        self.assertEqual(ssid.get('notes'), "Rogue AP")

        client = ssid.get('client')[0]
        self.assertEqual(client.get('type'), 'Server')
        self.assertEqual(client.get('name'), 'localhost')
        self.assertEqual(client.get('ip_v4'), '192.168.0.1')
        self.assertEqual(client.get('ip_v6'), '::1')

        resource = client.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

    def test_create_ssid_basic(self):
        body = {
            "name": "Base Station"
        }
        self.create_SSID(body)

        ssid = self.get_SSID(1)
        self.assertEqual(ssid.get('name'), "Base Station")
        self.assertEqual(ssid.get('client'), [])

    def test_create_ssid_basic_client(self):
        body = {
            "name": "Base Station",
            "client": [{
                "type": "Server"
            }]
        }
        self.create_SSID(body)

        ssid = self.get_SSID(1)
        self.assertEqual(ssid.get('name'), "Base Station")
        client = ssid.get('client')[0]
        self.assertEqual(client.get('type'), 'Server')
        self.assertEqual(client.get('resource'), [])

    def test_update_ssid(self):
        self.create_SSID(self.basic_ssid)
        self.update_SSID(1, self.extended_ssid)

        ssid = self.get_SSID(1)
        client = ssid.get('client')[1]
        self.assertEqual(client.get('type'), 'Client')
        self.assertEqual(client.get('name'), 'localhost')
        self.assertEqual(client.get('ip_v4'), '192.168.0.2')
        self.assertEqual(client.get('ip_v6'), '::2')

        resource = client.get('resource')[0]
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('type'), 'TCP')
        self.assertEqual(resource.get('notes'), 'Apache')

    def test_merge_ssid(self):
        self.create_SSID(self.basic_ssid)
        self.patch_SSID(1, {
            "crypto": "WPA2-PSK",
            "client": [{
                "id": 1,
                "type": "Router"
            }]

        })

        ssid = self.get_SSID(1)
        self.assertEqual(ssid.get('crypto'), 'WPA2-PSK')
        client = ssid.get('client')[0]
        self.assertEqual(client.get('type'), 'Router')

    def test_create_entity(self):
        self.create_entity(self.basic_entity)
        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), "Sky router")
        self.assertEqual(entity.get('notes'), "SKY+")
        self.assertEqual(entity.get('status'), "UP")
        self.assertEqual(entity.get('type'), "Server")
        self.assertEqual(entity.get('hardware'), "Sky")

        # Ensure the correct number of addresses
        self.assertEqual(len(entity.get('interface')), 1)
        interface = entity.get('interface')[0]
        self.assertEqual(interface.get('name'), 'localhost')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(interface.get('vendor'), 'Extel')

        resource = interface.get('resource')
        # Ensure the correct number of resources
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0].get('port'), 80)
        self.assertEqual(resource[0].get('type'), "TCP")
        self.assertEqual(resource[0].get('notes'), "Apache")
        self.assertEqual(resource[1].get('port'), 443)
        self.assertEqual(resource[1].get('type'), "TCP")
        self.assertEqual(resource[1].get('notes'), "NGINX")

    def test_create_entity_basic(self):
        basic = {
            "name": "tiny"
        }

        self.create_entity(basic)
        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), "tiny")
        self.assertEqual(entity.get('interface'), [])

    def test_create_entity_basic_interface(self):
        basic = {
            "name": "small",
            "interface": [
                {
                    "name": "broadband",
                }
            ]
        }

        self.create_entity(basic)
        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), "small")
        interface = entity.get('interface')[0]
        self.assertEqual(interface.get('name'), 'broadband')
        self.assertEqual(interface.get('resource'), [])

    def test_update_entity(self):
        self.create_entity(self.basic_entity)
        # Make sure we have the correct number of Addresses and Resources
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 2)

        self.update_entity(resource_id=1, resource=self.extended_entity)
        # Make sure we have the correct number of Addresses and Resources
        self.assertEqual(Interface.objects.all().count(), 2)
        self.assertEqual(Resource.objects.all().count(), 4)
        entity = self.get_entity(1)

        self.assertEqual(entity.get('name'), "Rogue Access Point")
        self.assertEqual(entity.get('notes'), "Rogue")
        self.assertEqual(entity.get('status'), "DOWN")
        self.assertEqual(entity.get('type'), "Server")
        self.assertEqual(entity.get('hardware'), "RaspberryPi")

        # Ensure the correct number of addresses
        self.assertEqual(len(entity.get('interface')), 2)

        address = entity.get('interface')[0]
        self.assertEqual(address.get('name'), 'hacked')
        self.assertEqual(address.get('ip_v4'), '10.0.0.1')
        self.assertEqual(address.get('ip_v6'), '::ff')
        self.assertEqual(address.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(address.get('vendor'), 'Extel')

        # Ensure the correct number of resources
        self.assertEqual(len(address.get('resource')), 2)
        resource = address.get('resource')
        self.assertEqual(resource[0].get('port'), 88)
        self.assertEqual(resource[0].get('type'), "UDP")
        self.assertEqual(resource[0].get('notes'), "Apache")
        self.assertEqual(resource[1].get('port'), 443)
        self.assertEqual(resource[1].get('type'), "TCP")
        self.assertEqual(resource[1].get('notes'), "NGINX")

        address = entity.get('interface')[1]
        self.assertEqual(address.get('name'), 'hostname')
        self.assertEqual(address.get('ip_v4'), '10.0.0.2')
        self.assertEqual(address.get('ip_v6'), '::2')
        self.assertEqual(address.get('physical_address'), '44:49:44:42:4a:41')
        self.assertEqual(address.get('vendor'), 'Antel')

        resource = address.get('resource')
        # Ensure the correct number of resources
        self.assertEqual(len(address.get('resource')), 2)
        self.assertEqual(resource[0].get('port'), 80)
        self.assertEqual(resource[0].get('type'), "TCP")
        self.assertEqual(resource[0].get('notes'), "Apache")
        self.assertEqual(resource[1].get('port'), 443)
        self.assertEqual(resource[1].get('type'), "TCP")
        self.assertEqual(resource[1].get('notes'), "NGINX")

        self.update_entity(resource_id=1, resource=self.basic_entity)
        # Make sure we have the correct number of Addresses and Resources
        self.assertEqual(Interface.objects.all().count(), 1)
        self.assertEqual(Resource.objects.all().count(), 2)

    def test_merge_entity(self):
        self.create_entity(self.basic_entity)

        self.patch_entity(resource_id=1, resource={
            "name": "modem",
            "hardware": "gibson",
            "interface": [{
                "id": 1,
                "name": "server",
            }]
        })

        entity = self.get_entity(1)
        self.assertEqual(entity.get('name'), 'modem')
        self.assertEqual(entity.get('hardware'), "gibson")

        # Ensure the correct number of addresses
        self.assertEqual(len(entity.get('interface')), 1)
        interface = entity.get('interface')[0]
        self.assertEqual(interface.get('name'), 'server')

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

    def test_combination(self):
        resource = {
            "id": 1,
            "port": 80,
            "type": "TCP",
            "notes": "Apache"
        }

        interface = {
            "id": 1,
            "type": "Server",
            "hardware": "Intel",
            "name": "localhost",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "physical_address": "33:39:34:32:3a:31",
            "vendor": "Extel",
            "notes": "local",
            "resource": [{
                "id": 2,
                "port": 80,
                "type": "TCP",
                "notes": "Apache"
            }],
        }

        entity = {
            "id": 1,
            "name": "Sky router",
            "notes": "SKY+",
            "type": "Server",
            "hardware": "Sky",
            "os": "Linux",
            "interface": [{
                "id": 2,
                "name": "localhost",
                "type": "wifi",
                "hardware": "ieee",
                "notes": "usb",
                "ip_v4": "192.168.0.1",
                "ip_v6": "::1",
                "resource": [{
                    "id": 3,
                    "port": 80,
                    "type": "TCP",
                    "notes": "Apache"
                }],
                "physical_address": "33:39:34:32:3a:31",
                "vendor": "Extel"
            }
            ],
            "status": "UP"
        }

        ssid = {
            "id": 1,
            "type": "WIFI_AP",
            "hardware": "Sky",
            "name": "Base Station",
            "channel": 10,
            "frequency": 10,
            "crypto": "WPA",
            "BSSID": "33:39:34:32:3a:31",
            "notes": "Rogue AP",
            "client": [{
                "id": 3,
                "name": "localhost",
                "type": "wifi",
                "hardware": "ieee",
                "notes": "usb",
                "ip_v4": "192.168.0.1",
                "ip_v6": "::1",
                "resource": [{
                    "id": 4,
                    "port": 80,
                    "type": "TCP",
                    "notes": "Apache"
                }],
                "physical_address": "33:39:34:32:3a:31",
                "vendor": "Extel"
            }
            ]
        }

        created_resource = self.create_resource({"port": 80}).data.get('id')
        self.patch_resource(created_resource, {"type": "TCP"})
        self.patch_resource(created_resource, {"notes": "Apache"})
        self.assertEqual(len(DeepDiff(self.get_resource(created_resource), resource)), 0)

        created_address = self.create_interface({"name": "localhost", "resource": [{"port": 80}]}).data.get('id')
        self.patch_interface(created_address, {"type": "Server"})
        self.patch_interface(created_address, {"hardware": "Intel"})
        self.patch_interface(created_address, {"name": "localhost"})
        self.patch_interface(created_address, {"ip_v4": "192.168.0.1"})
        self.patch_interface(created_address, {"ip_v6": "::1"})
        self.patch_interface(created_address, {"physical_address": "33:39:34:32:3a:31"})
        self.patch_interface(created_address, {"vendor": "Extel"})
        self.patch_interface(created_address, {"notes": "local"})
        self.patch_interface(created_address, {"resource": [{"id": 2, "type": "TCP"}]})
        self.patch_interface(created_address, {"resource": [{"id": 2, "notes": "Apache"}]})
        self.assertEqual(len(DeepDiff(self.get_interface(created_address), interface)), 0)

        created_entity = self.create_entity({"name": "Sky router",
                                             "interface": [
                                                 {"name": "localhost", "resource": [{"port": 80}]}
                                             ]}
                                            ).data.get('id')
        self.patch_entity(created_entity, {"notes": "SKY+"})
        self.patch_entity(created_entity, {"type": "Server"})
        self.patch_entity(created_entity, {"hardware": "Sky"})
        self.patch_entity(created_entity, {"os": "Linux"})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "ip_v4": "192.168.0.1"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "ip_v6": "::1"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "type": "wifi"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "hardware": "ieee"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "notes": "usb"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2,  "physical_address": "33:39:34:32:3a:31"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2,  "vendor": "Extel"}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "resource": [{"id": 3, "type": "TCP"}]}]})
        self.patch_entity(created_entity, {"interface": [{"id": 2, "resource": [{"id": 3, "notes": "Apache"}]}]})
        self.patch_entity(created_entity, {"status": "UP"})
        created = self.get_entity(created_entity)
        created.pop('first_seen')
        created.pop('last_seen')
        self.assertEqual(len(DeepDiff(created, entity)), 0)

        created_ssid = self.create_SSID({"type": "WIFI_AP",
                                         "client": [{"name": "localhost", "resource": [{"port": 80}]}
                                                    ]}
                                        ).data.get('id')
        self.patch_SSID(created_ssid, {"hardware": "Sky"})
        self.patch_SSID(created_ssid, {"name": "Base Station"})
        self.patch_SSID(created_ssid, {"channel": 10})
        self.patch_SSID(created_ssid, {"frequency": 10})
        self.patch_SSID(created_ssid, {"crypto": "WPA"})
        self.patch_SSID(created_ssid, {"BSSID": "33:39:34:32:3a:31"})
        self.patch_SSID(created_ssid, {"notes": "Rogue AP"})

        self.patch_SSID(created_ssid, {"client": [{"id": 3, "ip_v4": "192.168.0.1"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "ip_v6": "::1"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "type": "wifi"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "hardware": "ieee"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "notes": "usb"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "physical_address": "33:39:34:32:3a:31"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "vendor": "Extel"}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "resource": [{"id": 4, "type": "TCP"}]}]})
        self.patch_SSID(created_ssid, {"client": [{"id": 3, "resource": [{"id": 4, "notes": "Apache"}]}]})
        created = self.get_SSID(created_ssid)
        created.pop('first_seen')
        created.pop('last_seen')
        self.assertEqual(len(DeepDiff(created, ssid)), 0)


    # Helper methods

    def create_entity(self, resource):
        return self.post(table='entities', body=resource)

    def get_entity(self, resource_id):
        return self.get(table='entities', pk=resource_id)

    def update_entity(self, resource_id, resource):
        return self.put(table='entities', pk=resource_id, body=resource)

    def patch_entity(self, resource_id, resource):
        return self.patch(table='entities', pk=resource_id, body=resource)

    def delete_entity(self, resource_id, ignore_response=False):
        return self.delete(table='entities', pk=resource_id, ignore_response=ignore_response)

    def create_SSID(self, resource):
        return self.post(table='ssids', body=resource)

    def get_SSID(self, resource_id):
        return self.get(table='ssids', pk=resource_id)

    def update_SSID(self, resource_id, resource):
        return self.put(table='ssids', pk=resource_id, body=resource)

    def patch_SSID(self, resource_id, resource):
        return self.patch(table='ssids', pk=resource_id, body=resource)

    def delete_SSID(self, resource_id, ignore_response=False):
        return self.delete(table='ssids', pk=resource_id, ignore_response=ignore_response)

    def create_resource(self, resource):
        return self.post(table='resources', body=resource)

    def get_interface(self, resource_id):
        return self.get(table='interfaces', pk=resource_id)

    def update_interface(self, resource_id, resource):
        return self.put(table='interfaces', pk=resource_id, body=resource)

    def patch_interface(self, resource_id, resource):
        return self.patch(table='interfaces', pk=resource_id, body=resource)

    def delete_interface(self, resource_id, ignore_response=False):
        return self.delete(table='interfaces', pk=resource_id, ignore_response=ignore_response)

    def create_interface(self, resource):
        return self.post(table='interfaces', body=resource)

    def get_resource(self, resource_id):
        return self.get(table='resources', pk=resource_id)

    def update_resource(self, resource_id, resource):
        return self.put(table='resources', pk=resource_id, body=resource)

    def patch_resource(self, resource_id, resource):
        return self.patch(table='resources', pk=resource_id, body=resource)

    def delete_resource(self, resource_id, ignore_response=False):
        return self.delete(table='resources', pk=resource_id, ignore_response=ignore_response)

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

    def delete(self, table, pk, ignore_response=False):
        response = self.client.delete('/api/v1/{resource}/{pk}/'.format(resource=table, pk=pk),
                                      content_type='application/json')
        if not ignore_response:
            self.assertEqual(response.status_code, 204)
        return response
