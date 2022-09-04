import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from entity.models import Resource, Address, Entity


class EntityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.basic_entity = {
            "name": "Sky router",
            "notes": "SKY+",
            "type": "Router",
            "hardware": "Sky",
            "address": [
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

        cls.extended_entity = {
            "name": "Rogue Access Point",
            "notes": "Rogue",
            "type": "Hacker",
            "hardware": "RaspberryPi",
            "address": [
                {
                    "hostname": "localhost",
                    "ip_v4": "10.0.0.1",
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
            "status": "UP",
            "first_seen": "2022-09-03T09:39:20.922387",
            "last_seen": "2022-09-03T09:39:20.922387"
        }

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        self.client.post('/api/v1/entities/', self.basic_entity, content_type='application/json')
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_bad(self):
        response = self.client.post('/api/v1/entities/', {})
        self.assertEqual(response.status_code, 400)
        # todo assert error

    def test_post(self):
        self.create_entity()

    def test_get_model_top_level(self):
        entity = self.get_entity_model()

        self.assertEqual(entity.get('name'), "Sky router")
        self.assertEqual(entity.get('notes'), "SKY+")
        self.assertEqual(entity.get('status'), "UP")
        self.assertEqual(entity.get('type'), "Router")
        self.assertEqual(entity.get('hardware'), "Sky")

    def test_get_model_address(self):
        entity = self.get_entity_model()

        address = entity.get('address')[0]

        self.assertEqual(address.get('hostname'), 'localhost')
        self.assertEqual(address.get('ip_v4'), '192.168.0.1')
        self.assertEqual(address.get('ip_v6'), '::1')
        self.assertEqual(address.get('mac_address'), '33:39:34:32:3a:31')
        self.assertEqual(address.get('mac_vendor'), 'Extel')

        resource = address.get('resource')

        self.assertEqual(resource[0].get('port'), 80)
        self.assertEqual(resource[0].get('type'), "TCP")
        self.assertEqual(resource[0].get('notes'), "Apache")

        self.assertEqual(resource[1].get('port'), 443)
        self.assertEqual(resource[1].get('type'), "TCP")
        self.assertEqual(resource[1].get('notes'), "NGINX")

    def test_update_model(self):
        model = self.get_entity_model()
        model["name"] = "Updated Name"
        model["address"][0]["hostname"] = "new-host"
        model["address"][0]["ip_v4"] = "127.0.0.1"
        model["address"][0]["resource"][0]["notes"] = "Notes"

        self.update_entity_model(model)

        entity = self.get_entity_model()
        self.assertEqual(entity.get('name'), "Updated Name")

        address = entity.get('address')[0]
        self.assertEqual(address.get('hostname'), 'new-host')
        self.assertEqual(address.get('ip_v4'), '127.0.0.1')

        resource = address.get('resource')
        self.assertEqual(resource[0].get('notes'), "Notes")

    def test_swap_models(self):
        self.update_entity_model(self.extended_entity)

        addresses = Address.objects.all()
        resources = Resource.objects.all()

        # Two addresses
        self.assertEqual(addresses.count(), 2)

        # Two resources per address
        self.assertEqual(resources.count(), 4)

        self.update_entity_model(self.basic_entity)

        addresses = Address.objects.all()
        resources = Resource.objects.all()

        self.assertEqual(addresses.count(), 1)
        self.assertEqual(resources.count(), 2)



    # Helper methods

    def get_entity_model(self):
        response = self.client.get('/api/v1/entities/1/', kwargs={'pk': 1})
        self.assertEqual(response.status_code, 200)
        content = response.content
        model = json.loads(content)
        return model

    def update_entity_model(self, new_model):
        response = self.client.put('/api/v1/entities/1/', new_model, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def create_entity(self):
        response = self.client.post('/api/v1/entities/',
                                    {"name": "name", "address": [{"hostname": "host", "resource": []}]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
