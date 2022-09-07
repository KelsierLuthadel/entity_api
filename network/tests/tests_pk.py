import json
from deepdiff import DeepDiff
from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime

import iso8601
import datetime

from network.models import Site, Network, Switch, WiFi, Machine, Interface, Bluetooth, Radio, Resource
from network.tests.rest_helper import RestHelper

BASE_URL = '/api/v2/'


class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.public_site = {
            "name": "Public",
            "type": "Network",
            "notes": "Public Internet"
        }

        cls.private_site = {
            "name": "Private",
            "type": "Network",
            "notes": "Local network"
        }

        cls.interface_body = {
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.1",
            "ip_v6": "::1",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
        }

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        self.rest_helper = RestHelper(self.client, self.assertEqual)
        pass

    def tearDown(self):
        self.rest_helper.delete_site(1, True)
        self.rest_helper.delete_network(1, True)
        self.rest_helper.delete_switch(1, True)
        self.rest_helper.delete_wifi(1, True)
        self.rest_helper.delete_machine(1, True)
        self.rest_helper.delete_interface(1, True)
        self.rest_helper.delete_resource(1, True)
        self.rest_helper.delete_bluetooth(1, True)
        self.rest_helper.delete_radio(1, True)
        pass

    def test_network_create(self):
        public = self.rest_helper.create_site(self.public_site).data.get('id')
        private = self.rest_helper.create_site(self.private_site).data.get('id')

        # Create a public network
        self.rest_helper.create_network({
            "name": "Public Network",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": public
        })

        # Create a private network
        self.rest_helper.create_network({
            "name": "Private Network",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": private
        })

        # Create a second private network
        self.rest_helper.create_network({
            "name": "Sysadmin Network",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": private
        })

        self.assertEqual(len(Site.objects.all()), 2)
        self.assertEqual(len(Network.objects.all()), 3)
        self.assertEqual(len(Network.objects.filter(site_id=public)), 1)
        self.assertEqual(len(Network.objects.filter(site_id=private)), 2)

    def test_switch_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        # Create a public network
        network = self.rest_helper.create_network({
            "name": "Public Network",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_network = self.rest_helper.create_network({
            "name": "Public Network",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site
        })

        network_id = network.data.get('id')
        alt_network_id = alt_network.data.get('id')

        self.rest_helper.create_switch({
            "name": "PrivateNet",
            "address": "192.168.0.1",
            "mask": "255.255.255.0",
            "gateway": "10.0.0.1",
            "physical_address": "33:39:34:32:3a:31",
            "vendor": "Cisco",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": network_id
        })

        self.rest_helper.create_switch({
            "name": "AdminNet",
            "address": "192.168.1.1",
            "mask": "255.255.255.0",
            "gateway": "10.0.0.1",
            "physical_address": "43:39:34:32:3a:31",
            "vendor": "Cisco",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": network_id
        })

        self.rest_helper.create_switch({
            "name": "HiddenNet",
            "address": "192.168.2.1",
            "mask": "255.255.255.0",
            "gateway": "10.0.0.1",
            "physical_address": "13:39:34:32:3a:31",
            "vendor": "Cisco",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": alt_network_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Network.objects.all()), 2)
        self.assertEqual(len(Network.objects.filter(site_id=site)), 2)

        self.assertEqual(len(Switch.objects.all()), 3)
        self.assertEqual(len(Switch.objects.filter(site_id=network_id)), 3)
        self.assertEqual(len(Switch.objects.filter(network_id=network_id)), 2)
        self.assertEqual(len(Switch.objects.filter(network_id=alt_network_id)), 1)

    def test_wifi_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        # Create a public network
        network = self.rest_helper.create_network({
            "name": "Public Network",
            "type": "Wifi AP",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_network = self.rest_helper.create_network({
            "name": "Private Network",
            "type": "Wifi AP",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
            "site_id": site
        })

        network_id = network.data.get('id')
        alt_network_id = alt_network.data.get('id')

        self.rest_helper.create_wifi({
            "name": "Public Wireless",
            "type": "WIFI_AP",
            "address": "192.168.56.1",
            "mask": "255.255.255.0",
            "gateway": "172.16.0.1",
            "status": "UP",
            "channels": "11,15",
            "frequency": 1150,
            "crypto": "PSK",
            "SSID": "33:39:34:32:3a:31",
            "BSSID": "33:39:34:32:3a:32",
            "vendor": "HP",
            "notes": "Wifi AP",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": network_id
        })

        self.rest_helper.create_wifi({
            "name": "Public Wireless",
            "type": "WIFI_AP",
            "address": "192.168.57.1",
            "mask": "255.255.255.0",
            "gateway": "172.16.0.1",
            "status": "UP",
            "channels": "11,15",
            "frequency": 1150,
            "crypto": "PSK",
            "SSID": "23:39:34:32:3a:31",
            "BSSID": "23:39:34:32:3a:32",
            "vendor": "HP",
            "notes": "Wifi AP",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": network_id
        })

        self.rest_helper.create_wifi({
            "name": "Private Wireless",
            "type": "WIFI_AP",
            "address": "192.168.58.1",
            "mask": "255.255.255.0",
            "gateway": "172.16.0.1",
            "status": "UP",
            "channels": "11,15",
            "frequency": 1150,
            "crypto": "PSK",
            "SSID": "43:39:34:32:3a:31",
            "BSSID": "43:39:34:32:3a:32",
            "vendor": "HP",
            "notes": "Wifi AP",
            "detected_by": "ARP",
            "site_id": site,
            "network_id": alt_network_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Network.objects.all()), 2)
        self.assertEqual(len(Network.objects.filter(site_id=site)), 2)

        self.assertEqual(len(WiFi.objects.all()), 3)
        self.assertEqual(len(WiFi.objects.filter(site_id=network_id)), 3)
        self.assertEqual(len(WiFi.objects.filter(network_id=network_id)), 2)
        self.assertEqual(len(WiFi.objects.filter(network_id=alt_network_id)), 1)

    def test_machine_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Machine.objects.all()), 2)
        self.assertEqual(len(Machine.objects.filter(site_id=site)), 2)

    def test_interface_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        machine_id = machine.data.get('id')
        alt_machine_id = alt_machine.data.get('id')

        interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.2",
            "ip_v6": "::2",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        alt_interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.3",
            "ip_v6": "::3",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        hidden_interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.4",
            "ip_v6": "::4",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": alt_machine_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Machine.objects.all()), 2)
        self.assertEqual(len(Machine.objects.filter(site_id=site)), 2)

        self.assertEqual(len(Interface.objects.all()), 3)
        self.assertEqual(len(Interface.objects.filter(site_id=site)), 3)
        self.assertEqual(len(Interface.objects.filter(machine_id=machine_id)), 2)
        self.assertEqual(len(Interface.objects.filter(machine_id=alt_machine_id)), 1)

    def test_resource_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        machine_id = machine.data.get('id')
        alt_machine_id = alt_machine.data.get('id')

        interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.2",
            "ip_v6": "::2",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        alt_interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.3",
            "ip_v6": "::3",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        hidden_interface = self.rest_helper.create_interface({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.4",
            "ip_v6": "::4",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": alt_machine_id
        })

        interface_id = interface.data.get('id')
        alt_interface_id = alt_interface.data.get('id')
        hidden_interface_id = hidden_interface.data.get('id')

        apache = self.rest_helper.create_resource({
            "name": "Apache",
            "protocol": "TCP",
            "port": 80,
            "notes": "Server",
            "site_id": site,
            "interface_id": interface_id
        })

        apache_ssl = self.rest_helper.create_resource({
            "name": "Apache SSL",
            "protocol": "TCP",
            "port": 443,
            "notes": "Server",
            "site_id": site,
            "interface_id": interface_id
        })

        nginx = self.rest_helper.create_resource({
            "name": "NGINX",
            "protocol": "TCP",
            "port": 8080,
            "notes": "Server",
            "site_id": site,
            "interface_id": interface_id
        })

        audio = self.rest_helper.create_resource({
            "name": "Audio stream",
            "protocol": "UDP",
            "port": 445,
            "notes": "Server",
            "site_id": site,
            "interface_id": alt_interface_id
        })

        video = self.rest_helper.create_resource({
            "name": "Video stream",
            "protocol": "UDP",
            "port": 8445,
            "notes": "Server",
            "site_id": site,
            "interface_id": hidden_interface_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Machine.objects.all()), 2)
        self.assertEqual(len(Machine.objects.filter(site_id=site)), 2)

        self.assertEqual(len(Interface.objects.all()), 3)
        self.assertEqual(len(Interface.objects.filter(site_id=site)), 3)
        self.assertEqual(len(Interface.objects.filter(machine_id=machine_id)), 2)
        self.assertEqual(len(Interface.objects.filter(machine_id=alt_machine_id)), 1)

        self.assertEqual(len(Resource.objects.all()), 5)
        self.assertEqual(len(Resource.objects.filter(site_id=site)), 5)
        self.assertEqual(len(Resource.objects.filter(interface_id=interface_id)), 3)
        self.assertEqual(len(Resource.objects.filter(interface_id=alt_interface_id)), 1)
        self.assertEqual(len(Resource.objects.filter(interface_id=hidden_interface_id)), 1)

    def test_bluetooth_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        machine_id = machine.data.get('id')
        alt_machine_id = alt_machine.data.get('id')

        bluetooth = self.rest_helper.create_bluetooth({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.2",
            "ip_v6": "::2",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        alt_interface = self.rest_helper.create_bluetooth({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.3",
            "ip_v6": "::3",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        hidden_interface = self.rest_helper.create_bluetooth({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.4",
            "ip_v6": "::4",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": alt_machine_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Machine.objects.all()), 2)
        self.assertEqual(len(Machine.objects.filter(site_id=site)), 2)

        self.assertEqual(len(Bluetooth.objects.all()), 3)
        self.assertEqual(len(Bluetooth.objects.filter(site_id=site)), 3)
        self.assertEqual(len(Bluetooth.objects.filter(machine_id=machine_id)), 2)
        self.assertEqual(len(Bluetooth.objects.filter(machine_id=alt_machine_id)), 1)

    def test_radio_create(self):
        site = self.rest_helper.create_site(self.public_site).data.get('id')

        machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        alt_machine = self.rest_helper.create_machine({
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
            "site_id": site
        })

        machine_id = machine.data.get('id')
        alt_machine_id = alt_machine.data.get('id')

        bluetooth = self.rest_helper.create_radio({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.2",
            "ip_v6": "::2",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        alt_interface = self.rest_helper.create_radio({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.3",
            "ip_v6": "::3",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": machine_id
        })

        hidden_interface = self.rest_helper.create_radio({
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "ip_v4": "192.168.0.4",
            "ip_v6": "::4",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
            "site_id": site,
            "machine_id": alt_machine_id
        })

        self.assertEqual(len(Site.objects.all()), 1)
        self.assertEqual(len(Machine.objects.all()), 2)
        self.assertEqual(len(Machine.objects.filter(site_id=site)), 2)

        self.assertEqual(len(Radio.objects.all()), 3)
        self.assertEqual(len(Radio.objects.filter(site_id=site)), 3)
        self.assertEqual(len(Radio.objects.filter(machine_id=machine_id)), 2)
        self.assertEqual(len(Radio.objects.filter(machine_id=alt_machine_id)), 1)
