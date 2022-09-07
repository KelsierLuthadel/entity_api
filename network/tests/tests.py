import json
from deepdiff import DeepDiff
from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime

import iso8601
import datetime

BASE_URL = '/api/v2/'


class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.site_body = {
            "name": "Home",
            "type": "Local Network",
            "notes": "Home test network"
        }

        cls.network_body = {
            "name": "PrivateNet",
            "type": "Switch",
            "os": "Cisco",
            "hardware": "HP",
            "status": "UP",
            "notes": "Local Switch",
            "detected_by": "ARP",
        }

        cls.switch_body = {
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
        }

        cls.wifi_body = {
            "name": "Wireless",
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
        }

        cls.machine_body = {
            "name": "Laptop",
            "type": "Laptop",
            "os": "Windows",
            "hardware": "Intel",
            "status": "UP",
            "notes": "Dev Machine",
            "detected_by": "ARP",
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

        cls.resource_body = {
            "name": "Apache",
            "protocol": "TCP",
            "port": 80,
            "notes": "Server",
        }

        cls.bluetooth_body = {
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
        }

        cls.radio_body = {
            "name": "Adapter",
            "type": "Wireless",
            "hardware": "Intel",
            "physical_address": "f0:0d:ca:fe:be:ef",
            "vendor": "Belkin",
            "status": "UP",
            "notes": "Local Network",
        }

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        pass

    def tearDown(self):
        self.delete_site(1, True)
        self.delete_network(1, True)
        self.delete_switch(1, True)
        self.delete_wifi(1, True)
        self.delete_machine(1, True)
        self.delete_interface(1, True)
        self.delete_resource(1, True)
        self.delete_bluetooth(1, True)
        self.delete_radio(1, True)
        pass

    def test_site_create(self):
        self.create_site(self.site_body)
        site = self.get_site(1)
        self.assertEqual(site.get('name'), 'Home')
        self.assertEqual(site.get('type'), 'Local Network')
        self.assertEqual(site.get('notes'), 'Home test network')

    def test_site_put(self):
        self.create_site(self.site_body)
        update = {
            "name": "Work",
            "type": "Work Network",
            "notes": "Work test network"
        }
        self.update_site(resource_id=1, resource=update)

        site = self.get_site(1)
        self.assertEqual(site.get('name'), 'Work')
        self.assertEqual(site.get('type'), 'Work Network')
        self.assertEqual(site.get('notes'), 'Work test network')

    def test_site_patch(self):
        self.create_site(self.site_body)
        self.patch_site(1, resource={"name": 'Private'})
        self.patch_site(1, resource={"type": 'Private Network'})
        self.patch_site(1, resource={"notes": 'Private test network'})
        site = self.get_site(1)
        self.assertEqual(site.get('name'), 'Private')
        self.assertEqual(site.get('type'), 'Private Network')
        self.assertEqual(site.get('notes'), 'Private test network')

    def test_network_create(self):
        self.create_network(self.network_body)
        network = self.get_network(1)
        self.assertEqual(network.get('name'), 'PrivateNet')
        self.assertEqual(network.get('type'), 'Switch')
        self.assertEqual(network.get('os'), 'Cisco')
        self.assertEqual(network.get('hardware'), 'HP')
        self.assertEqual(network.get('status'), 'UP')
        self.assertEqual(network.get('notes'), 'Local Switch')
        self.assertEqual(network.get('detected_by'), 'ARP')

    def test_network_put(self):
        self.create_network(self.network_body)
        update = {
            "name": "Anonymous",
            "type": "Switch",
            "os": "Netgear",
            "hardware": "Netgear",
            "status": "DOWN",
            "notes": "Proxy",
            "detected_by": "ARP",
            "last_seen": datetime.datetime.utcnow()
        }
        self.update_network(resource_id=1, resource=update)

        network = self.get_network(1)
        self.assertEqual(network.get('name'), 'Anonymous')
        self.assertEqual(network.get('type'), 'Switch')
        self.assertEqual(network.get('os'), 'Netgear')
        self.assertEqual(network.get('hardware'), 'Netgear')
        self.assertEqual(network.get('status'), 'DOWN')
        self.assertEqual(network.get('notes'), 'Proxy')
        self.assertEqual(network.get('detected_by'), 'ARP')
        self.is_date_newer(network.get('first_seen'), network.get('last_seen'))

    def test_network_patch(self):
        self.create_network(self.network_body)
        self.patch_network(1, resource={"name": 'Public'})
        self.patch_network(1, resource={"type": 'Router'})
        self.patch_network(1, resource={"os": 'Unknown'})
        self.patch_network(1, resource={"hardware": 'Proprietary'})
        self.patch_network(1, resource={"status": 'UP'})
        self.patch_network(1, resource={"notes": 'Shared internet'})
        self.patch_network(1, resource={"detected_by": 'ping'})
        self.patch_network(1, resource={"last_seen": datetime.datetime.utcnow()})
        network = self.get_network(1)
        self.assertEqual(network.get('name'), 'Public')
        self.assertEqual(network.get('type'), 'Router')
        self.assertEqual(network.get('os'), 'Unknown')
        self.assertEqual(network.get('hardware'), 'Proprietary')
        self.assertEqual(network.get('status'), 'UP')
        self.assertEqual(network.get('notes'), 'Shared internet')
        self.assertEqual(network.get('detected_by'), 'ping')
        self.is_date_newer(network.get('first_seen'), network.get('last_seen'))

    def test_switch_create(self):
        self.create_switch(self.switch_body)
        network = self.get_switch(1)
        self.assertEqual(network.get('name'), 'PrivateNet')
        self.assertEqual(network.get('address'), '192.168.0.1')
        self.assertEqual(network.get('mask'), '255.255.255.0')
        self.assertEqual(network.get('gateway'), '10.0.0.1')
        self.assertEqual(network.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(network.get('vendor'), 'Cisco')
        self.assertEqual(network.get('type'), 'Switch')
        self.assertEqual(network.get('os'), 'Cisco')
        self.assertEqual(network.get('hardware'), 'HP')
        self.assertEqual(network.get('status'), 'UP')
        self.assertEqual(network.get('notes'), 'Local Switch')
        self.assertEqual(network.get('detected_by'), 'ARP')

    def test_switch_put(self):
        self.create_switch(self.switch_body)
        update = {
            "name": "GibsonNet",
            "address": "192.168.89.2",
            "mask": "255.255.255.0",
            "gateway": "10.10.0.1",
            "physical_address": "be:ef:ca:fe:f0:0d",
            "vendor": "Gibson",
            "type": "Hub",
            "os": "Gibson",
            "hardware": "Hacked",
            "status": "UP",
            "notes": "Hack the Gibson",
            "detected_by": "ARP",
        }
        self.update_switch(resource_id=1, resource=update)

        switch = self.get_switch(1)
        self.assertEqual(switch.get('name'), 'GibsonNet')
        self.assertEqual(switch.get('address'), '192.168.89.2')
        self.assertEqual(switch.get('mask'), '255.255.255.0')
        self.assertEqual(switch.get('gateway'), '10.10.0.1')
        self.assertEqual(switch.get('physical_address'), 'be:ef:ca:fe:f0:0d')
        self.assertEqual(switch.get('vendor'), 'Gibson')
        self.assertEqual(switch.get('type'), 'Hub')
        self.assertEqual(switch.get('os'), 'Gibson')
        self.assertEqual(switch.get('hardware'), 'Hacked')
        self.assertEqual(switch.get('status'), 'UP')
        self.assertEqual(switch.get('notes'), 'Hack the Gibson')
        self.assertEqual(switch.get('detected_by'), 'ARP')

    def test_switch_patch(self):
        self.create_switch(self.switch_body)
        self.patch_switch(1, resource={"name": 'Owner'})
        self.patch_switch(1, resource={"type": 'Device'})
        self.patch_switch(1, resource={"os": 'Exxon'})
        self.patch_switch(1, resource={"hardware": 'Unknown'})
        self.patch_switch(1, resource={"status": 'DOWN'})
        self.patch_switch(1, resource={"notes": 'Unknown device'})
        self.patch_switch(1, resource={"detected_by": 'ping'})
        self.patch_switch(1, resource={"last_seen": datetime.datetime.utcnow()})
        switch = self.get_switch(1)
        self.assertEqual(switch.get('name'), 'Owner')
        self.assertEqual(switch.get('address'), '192.168.0.1')
        self.assertEqual(switch.get('mask'), '255.255.255.0')
        self.assertEqual(switch.get('gateway'), '10.0.0.1')
        self.assertEqual(switch.get('physical_address'), '33:39:34:32:3a:31')
        self.assertEqual(switch.get('vendor'), 'Cisco')
        self.assertEqual(switch.get('type'), 'Device')
        self.assertEqual(switch.get('os'), 'Exxon')
        self.assertEqual(switch.get('hardware'), 'Unknown')
        self.assertEqual(switch.get('status'), 'DOWN')
        self.assertEqual(switch.get('notes'), 'Unknown device')
        self.assertEqual(switch.get('detected_by'), 'ping')

    def test_wifi_create(self):
        self.create_wifi(self.wifi_body)
        wifi = self.get_wifi(1)
        self.assertEqual(wifi.get('name'), 'Wireless')
        self.assertEqual(wifi.get('address'), '192.168.56.1')
        self.assertEqual(wifi.get('mask'), '255.255.255.0')
        self.assertEqual(wifi.get('gateway'), '172.16.0.1')
        self.assertEqual(wifi.get('status'), 'UP')
        self.assertEqual(wifi.get('channels'), '11,15')
        self.assertEqual(wifi.get('frequency'), 1150)
        self.assertEqual(wifi.get('crypto'), 'PSK')
        self.assertEqual(wifi.get('SSID'), '33:39:34:32:3a:31')
        self.assertEqual(wifi.get('BSSID'), '33:39:34:32:3a:32')
        self.assertEqual(wifi.get('vendor'), 'HP')
        self.assertEqual(wifi.get('notes'), 'Wifi AP')
        self.assertEqual(wifi.get('detected_by'), 'ARP')

    def test_wifi_put(self):
        self.create_wifi(self.wifi_body)
        update = {
            "name": "Wireless Hub",
            "type": "WIFI_AD_HOC",
            "address": "192.168.57.2",
            "mask": "255.255.255.0",
            "gateway": "172.0.0.1",
            "status": "UP",
            "channels": "11,15",
            "frequency": 1150,
            "crypto": "PSK",
            "SSID": "33:39:34:32:3a:31",
            "BSSID": "33:39:34:32:3a:32",
            "vendor": "HP",
            "notes": "Wifi AP",
            "detected_by": "ARP",
        }
        self.update_wifi(resource_id=1, resource=update)

        wifi = self.get_wifi(1)
        self.assertEqual(wifi.get('name'), 'Wireless Hub')
        self.assertEqual(wifi.get('type'), 'WIFI_AD_HOC')
        self.assertEqual(wifi.get('address'), '192.168.57.2')
        self.assertEqual(wifi.get('mask'), '255.255.255.0')
        self.assertEqual(wifi.get('gateway'), '172.0.0.1')
        self.assertEqual(wifi.get('status'), 'UP')
        self.assertEqual(wifi.get('channels'), '11,15')
        self.assertEqual(wifi.get('frequency'), 1150)
        self.assertEqual(wifi.get('crypto'), 'PSK')
        self.assertEqual(wifi.get('SSID'), '33:39:34:32:3a:31')
        self.assertEqual(wifi.get('BSSID'), '33:39:34:32:3a:32')
        self.assertEqual(wifi.get('vendor'), 'HP')
        self.assertEqual(wifi.get('notes'), 'Wifi AP')
        self.assertEqual(wifi.get('detected_by'), 'ARP')

    def test_wifi_patch(self):
        self.create_wifi(self.wifi_body)
        self.patch_wifi(1, resource={"name": 'Home Net'})
        self.patch_wifi(1, resource={"type": 'WIFI_BRIDGED'})
        self.patch_wifi(1, resource={"address": '192.168.57.2'})
        self.patch_wifi(1, resource={"mask": '255.255.0.0'})
        self.patch_wifi(1, resource={"gateway": '1.10.0.1'})
        self.patch_wifi(1, resource={"status": 'DOWN'})
        self.patch_wifi(1, resource={"channels": '5,7,6'})
        self.patch_wifi(1, resource={"frequency": 11750})
        self.patch_wifi(1, resource={"crypto": 'None'})
        self.patch_wifi(1, resource={"SSID": 'f0:0d:ca:fe:be:ef'})
        self.patch_wifi(1, resource={"BSSID": 'be:ef:be:ef:be:ef'})
        self.patch_wifi(1, resource={"vendor": 'None'})
        self.patch_wifi(1, resource={"notes": 'Limited device'})
        self.patch_wifi(1, resource={"detected_by": 'ping'})
        self.patch_wifi(1, resource={"last_seen": datetime.datetime.utcnow()})
        wifi = self.get_wifi(1)
        self.assertEqual(wifi.get('name'), 'Home Net')
        self.assertEqual(wifi.get('type'), 'WIFI_BRIDGED')
        self.assertEqual(wifi.get('address'), '192.168.57.2')
        self.assertEqual(wifi.get('mask'), '255.255.0.0')
        self.assertEqual(wifi.get('gateway'), '1.10.0.1')
        self.assertEqual(wifi.get('status'), 'DOWN')
        self.assertEqual(wifi.get('channels'), '5,7,6')
        self.assertEqual(wifi.get('frequency'), 11750)
        self.assertEqual(wifi.get('crypto'), 'None')
        self.assertEqual(wifi.get('SSID'), 'f0:0d:ca:fe:be:ef')
        self.assertEqual(wifi.get('BSSID'), 'be:ef:be:ef:be:ef')
        self.assertEqual(wifi.get('vendor'), 'None')
        self.assertEqual(wifi.get('notes'), 'Limited device')
        self.assertEqual(wifi.get('detected_by'), 'ping')

    def test_machine_create(self):
        self.create_machine(self.machine_body)
        machine = self.get_machine(1)
        self.assertEqual(machine.get('name'), 'Laptop')
        self.assertEqual(machine.get('type'), 'Laptop')
        self.assertEqual(machine.get('os'), 'Windows')
        self.assertEqual(machine.get('hardware'), 'Intel')
        self.assertEqual(machine.get('status'), 'UP')
        self.assertEqual(machine.get('notes'), 'Dev Machine')
        self.assertEqual(machine.get('detected_by'), 'ARP')

    def test_machine_put(self):
        self.create_machine(self.machine_body)
        update = {
            "name": "Desktop",
            "type": "Desktop",
            "os": "Linux",
            "hardware": "Intel",
            "status": "DOWN",
            "notes": "Server",
            "detected_by": "ping",
        }
        self.update_machine(resource_id=1, resource=update)

        machine = self.get_machine(1)
        self.assertEqual(machine.get('name'), 'Desktop')
        self.assertEqual(machine.get('type'), 'Desktop')
        self.assertEqual(machine.get('os'), 'Linux')
        self.assertEqual(machine.get('hardware'), 'Intel')
        self.assertEqual(machine.get('status'), 'DOWN')
        self.assertEqual(machine.get('notes'), 'Server')
        self.assertEqual(machine.get('detected_by'), 'ping')

    def test_machine_patch(self):
        self.create_machine(self.machine_body)
        self.patch_machine(1, resource={"name": 'IOT'})
        self.patch_machine(1, resource={"type": 'Device'})
        self.patch_machine(1, resource={"os": 'Exxon'})
        self.patch_machine(1, resource={"hardware": 'Unknown'})
        self.patch_machine(1, resource={"status": 'DOWN'})
        self.patch_machine(1, resource={"notes": 'Unknown device'})
        self.patch_machine(1, resource={"detected_by": 'ping'})
        self.patch_machine(1, resource={"last_seen": datetime.datetime.utcnow()})
        machine = self.get_machine(1)
        self.assertEqual(machine.get('name'), 'IOT')
        self.assertEqual(machine.get('type'), 'Device')
        self.assertEqual(machine.get('os'), 'Exxon')
        self.assertEqual(machine.get('hardware'), 'Unknown')
        self.assertEqual(machine.get('status'), 'DOWN')
        self.assertEqual(machine.get('notes'), 'Unknown device')
        self.assertEqual(machine.get('detected_by'), 'ping')

    def test_interface_create(self):
        self.create_interface(self.interface_body)
        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'Adapter')
        self.assertEqual(interface.get('type'), 'Wireless')
        self.assertEqual(interface.get('hardware'), 'Intel')
        self.assertEqual(interface.get('ip_v4'), '192.168.0.1')
        self.assertEqual(interface.get('ip_v6'), '::1')
        self.assertEqual(interface.get('physical_address'), 'f0:0d:ca:fe:be:ef')
        self.assertEqual(interface.get('vendor'), 'Belkin')
        self.assertEqual(interface.get('status'), 'UP')
        self.assertEqual(interface.get('notes'), 'Local Network')

    def test_interface_put(self):
        self.create_interface(self.interface_body)
        update = {
            "name": "LAN",
            "type": "LAN",
            "hardware": "Intel",
            "ip_v4": "192.168.56.1",
            "ip_v6": "::2",
            "physical_address": "ca:fe:f0:0d:be:ef",
            "vendor": "Intel",
            "status": "UP",
            "notes": "Local LAN",
        }
        self.update_interface(resource_id=1, resource=update)

        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'LAN')
        self.assertEqual(interface.get('type'), 'LAN')
        self.assertEqual(interface.get('hardware'), 'Intel')
        self.assertEqual(interface.get('ip_v4'), '192.168.56.1')
        self.assertEqual(interface.get('ip_v6'), '::2')
        self.assertEqual(interface.get('physical_address'), 'ca:fe:f0:0d:be:ef')
        self.assertEqual(interface.get('vendor'), 'Intel')
        self.assertEqual(interface.get('status'), 'UP')
        self.assertEqual(interface.get('notes'), 'Local LAN')

    def test_interface_patch(self):
        self.create_interface(self.interface_body)
        self.patch_interface(1, resource={"name": 'WAN'})
        self.patch_interface(1, resource={"type": 'LAN'})
        self.patch_interface(1, resource={"hardware": 'Unknown'})
        self.patch_interface(1, resource={"ip_v4": '10.0.0.1'})
        self.patch_interface(1, resource={"ip_v6": '::3'})
        self.patch_interface(1, resource={"physical_address": 'be:ef:be:ef:be:ef'})
        self.patch_interface(1, resource={"vendor": 'Unknown'})
        self.patch_interface(1, resource={"status": 'DOWN'})
        self.patch_interface(1, resource={"notes": 'Unknown device'})
        self.patch_interface(1, resource={"last_seen": datetime.datetime.utcnow()})
        interface = self.get_interface(1)
        self.assertEqual(interface.get('name'), 'WAN')
        self.assertEqual(interface.get('type'), 'LAN')
        self.assertEqual(interface.get('hardware'), 'Unknown')
        self.assertEqual(interface.get('physical_address'), 'be:ef:be:ef:be:ef')
        self.assertEqual(interface.get('vendor'), 'Unknown')
        self.assertEqual(interface.get('status'), 'DOWN')
        self.assertEqual(interface.get('notes'), 'Unknown device')

    def test_resource_create(self):
        self.create_resource(self.resource_body)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('name'), 'Apache')
        self.assertEqual(resource.get('protocol'), 'TCP')
        self.assertEqual(resource.get('port'), 80)
        self.assertEqual(resource.get('notes'), 'Server')

    def test_resource_put(self):
        self.create_resource(self.resource_body)
        update = {
            "name": "Stream",
            "protocol": "UDP",
            "port": 1267,
            "notes": "Audio",
        }
        self.update_resource(resource_id=1, resource=update)
        resource = self.get_resource(1)
        self.assertEqual(resource.get('name'), 'Stream')
        self.assertEqual(resource.get('protocol'), 'UDP')
        self.assertEqual(resource.get('port'), 1267)
        self.assertEqual(resource.get('notes'), 'Audio')

    def test_resource_patch(self):
        self.create_resource(self.resource_body)
        self.patch_resource(1, resource={"name": 'CCTV'})
        self.patch_resource(1, resource={"protocol": 'UDP'})
        self.patch_resource(1, resource={"port": 4765})
        self.patch_resource(1, resource={"notes": 'Video'})
        resource = self.get_resource(1)
        self.assertEqual(resource.get('name'), 'CCTV')
        self.assertEqual(resource.get('protocol'), 'UDP')
        self.assertEqual(resource.get('port'), 4765)
        self.assertEqual(resource.get('notes'), 'Video')

    def test_bluetooth_create(self):
        self.create_bluetooth(self.bluetooth_body)
        bluetooth = self.get_bluetooth(1)
        self.assertEqual(bluetooth.get('name'), 'Adapter')
        self.assertEqual(bluetooth.get('type'), 'Wireless')
        self.assertEqual(bluetooth.get('hardware'), 'Intel')
        self.assertEqual(bluetooth.get('physical_address'), 'f0:0d:ca:fe:be:ef')
        self.assertEqual(bluetooth.get('vendor'), 'Belkin')
        self.assertEqual(bluetooth.get('status'), 'UP')
        self.assertEqual(bluetooth.get('notes'), 'Local Network')

    def test_bluetooth_put(self):
        self.create_bluetooth(self.bluetooth_body)
        update = {
            "name": "LAN",
            "type": "LAN",
            "hardware": "Intel",
            "physical_address": "ca:fe:f0:0d:be:ef",
            "vendor": "Intel",
            "status": "UP",
            "notes": "Local LAN",
        }
        self.update_bluetooth(resource_id=1, resource=update)

        bluetooth = self.get_bluetooth(1)
        self.assertEqual(bluetooth.get('name'), 'LAN')
        self.assertEqual(bluetooth.get('type'), 'LAN')
        self.assertEqual(bluetooth.get('hardware'), 'Intel')
        self.assertEqual(bluetooth.get('physical_address'), 'ca:fe:f0:0d:be:ef')
        self.assertEqual(bluetooth.get('vendor'), 'Intel')
        self.assertEqual(bluetooth.get('status'), 'UP')
        self.assertEqual(bluetooth.get('notes'), 'Local LAN')

    def test_bluetooth_patch(self):
        self.create_bluetooth(self.bluetooth_body)
        self.patch_bluetooth(1, resource={"name": 'WAN'})
        self.patch_bluetooth(1, resource={"type": 'LAN'})
        self.patch_bluetooth(1, resource={"hardware": 'Unknown'})
        self.patch_bluetooth(1, resource={"physical_address": 'be:ef:be:ef:be:ef'})
        self.patch_bluetooth(1, resource={"vendor": 'Unknown'})
        self.patch_bluetooth(1, resource={"status": 'DOWN'})
        self.patch_bluetooth(1, resource={"notes": 'Unknown device'})
        self.patch_bluetooth(1, resource={"last_seen": datetime.datetime.utcnow()})
        bluetooth = self.get_bluetooth(1)
        self.assertEqual(bluetooth.get('name'), 'WAN')
        self.assertEqual(bluetooth.get('type'), 'LAN')
        self.assertEqual(bluetooth.get('hardware'), 'Unknown')
        self.assertEqual(bluetooth.get('physical_address'), 'be:ef:be:ef:be:ef')
        self.assertEqual(bluetooth.get('vendor'), 'Unknown')
        self.assertEqual(bluetooth.get('status'), 'DOWN')
        self.assertEqual(bluetooth.get('notes'), 'Unknown device')

    def test_radio_create(self):
        self.create_radio(self.radio_body)
        radio = self.get_radio(1)
        self.assertEqual(radio.get('name'), 'Adapter')
        self.assertEqual(radio.get('type'), 'Wireless')
        self.assertEqual(radio.get('hardware'), 'Intel')
        self.assertEqual(radio.get('physical_address'), 'f0:0d:ca:fe:be:ef')
        self.assertEqual(radio.get('vendor'), 'Belkin')
        self.assertEqual(radio.get('status'), 'UP')
        self.assertEqual(radio.get('notes'), 'Local Network')

    def test_radio_put(self):
        self.create_radio(self.radio_body)
        update = {
            "name": "LAN",
            "type": "LAN",
            "hardware": "Intel",
            "physical_address": "ca:fe:f0:0d:be:ef",
            "vendor": "Intel",
            "status": "UP",
            "notes": "Local LAN",
        }
        self.update_radio(resource_id=1, resource=update)

        radio = self.get_radio(1)
        self.assertEqual(radio.get('name'), 'LAN')
        self.assertEqual(radio.get('type'), 'LAN')
        self.assertEqual(radio.get('hardware'), 'Intel')
        self.assertEqual(radio.get('physical_address'), 'ca:fe:f0:0d:be:ef')
        self.assertEqual(radio.get('vendor'), 'Intel')
        self.assertEqual(radio.get('status'), 'UP')
        self.assertEqual(radio.get('notes'), 'Local LAN')

    def test_radio_patch(self):
        self.create_radio(self.radio_body)
        self.patch_radio(1, resource={"name": 'WAN'})
        self.patch_radio(1, resource={"type": 'LAN'})
        self.patch_radio(1, resource={"hardware": 'Unknown'})
        self.patch_radio(1, resource={"physical_address": 'be:ef:be:ef:be:ef'})
        self.patch_radio(1, resource={"vendor": 'Unknown'})
        self.patch_radio(1, resource={"status": 'DOWN'})
        self.patch_radio(1, resource={"notes": 'Unknown device'})
        self.patch_radio(1, resource={"last_seen": datetime.datetime.utcnow()})
        radio = self.get_radio(1)
        self.assertEqual(radio.get('name'), 'WAN')
        self.assertEqual(radio.get('type'), 'LAN')
        self.assertEqual(radio.get('hardware'), 'Unknown')
        self.assertEqual(radio.get('physical_address'), 'be:ef:be:ef:be:ef')
        self.assertEqual(radio.get('vendor'), 'Unknown')
        self.assertEqual(radio.get('status'), 'DOWN')
        self.assertEqual(radio.get('notes'), 'Unknown device')

    # Helper methods

    def create_site(self, resource):
        return self.post(table='sites', body=resource)

    def get_site(self, resource_id):
        return self.get(table='sites', pk=resource_id)

    def update_site(self, resource_id, resource):
        return self.put(table='sites', pk=resource_id, body=resource)

    def patch_site(self, resource_id, resource):
        return self.patch(table='sites', pk=resource_id, body=resource)

    def delete_site(self, resource_id, ignore_response=False):
        return self.delete(table='sites', pk=resource_id, ignore_response=ignore_response)

    def create_network(self, resource):
        return self.post(table='networks', body=resource)

    def get_network(self, resource_id):
        return self.get(table='networks', pk=resource_id)

    def update_network(self, resource_id, resource):
        return self.put(table='networks', pk=resource_id, body=resource)

    def patch_network(self, resource_id, resource):
        return self.patch(table='networks', pk=resource_id, body=resource)

    def delete_network(self, resource_id, ignore_response=False):
        return self.delete(table='networks', pk=resource_id, ignore_response=ignore_response)

    def create_switch(self, resource):
        return self.post(table='switches', body=resource)

    def get_switch(self, resource_id):
        return self.get(table='switches', pk=resource_id)

    def update_switch(self, resource_id, resource):
        return self.put(table='switches', pk=resource_id, body=resource)

    def patch_switch(self, resource_id, resource):
        return self.patch(table='switches', pk=resource_id, body=resource)

    def delete_switch(self, resource_id, ignore_response=False):
        return self.delete(table='switches', pk=resource_id, ignore_response=ignore_response)

    def create_wifi(self, resource):
        return self.post(table='wifis', body=resource)

    def get_wifi(self, resource_id):
        return self.get(table='wifis', pk=resource_id)

    def update_wifi(self, resource_id, resource):
        return self.put(table='wifis', pk=resource_id, body=resource)

    def patch_wifi(self, resource_id, resource):
        return self.patch(table='wifis', pk=resource_id, body=resource)

    def delete_wifi(self, resource_id, ignore_response=False):
        return self.delete(table='wifis', pk=resource_id, ignore_response=ignore_response)

    def create_machine(self, resource):
        return self.post(table='machines', body=resource)

    def get_machine(self, resource_id):
        return self.get(table='machines', pk=resource_id)

    def update_machine(self, resource_id, resource):
        return self.put(table='machines', pk=resource_id, body=resource)

    def patch_machine(self, resource_id, resource):
        return self.patch(table='machines', pk=resource_id, body=resource)

    def delete_machine(self, resource_id, ignore_response=False):
        return self.delete(table='machines', pk=resource_id, ignore_response=ignore_response)

    def create_interface(self, resource):
        return self.post(table='interfaces', body=resource)

    def get_interface(self, resource_id):
        return self.get(table='interfaces', pk=resource_id)

    def update_interface(self, resource_id, resource):
        return self.put(table='interfaces', pk=resource_id, body=resource)

    def patch_interface(self, resource_id, resource):
        return self.patch(table='interfaces', pk=resource_id, body=resource)

    def delete_interface(self, resource_id, ignore_response=False):
        return self.delete(table='interfaces', pk=resource_id, ignore_response=ignore_response)

    def create_resource(self, resource):
        return self.post(table='resources', body=resource)

    def get_resource(self, resource_id):
        return self.get(table='resources', pk=resource_id)

    def update_resource(self, resource_id, resource):
        return self.put(table='resources', pk=resource_id, body=resource)

    def patch_resource(self, resource_id, resource):
        return self.patch(table='resources', pk=resource_id, body=resource)

    def delete_resource(self, resource_id, ignore_response=False):
        return self.delete(table='resources', pk=resource_id, ignore_response=ignore_response)

    def create_bluetooth(self, resource):
        return self.post(table='bluetooths', body=resource)

    def get_bluetooth(self, resource_id):
        return self.get(table='bluetooths', pk=resource_id)

    def update_bluetooth(self, resource_id, resource):
        return self.put(table='bluetooths', pk=resource_id, body=resource)

    def patch_bluetooth(self, resource_id, resource):
        return self.patch(table='bluetooths', pk=resource_id, body=resource)

    def delete_bluetooth(self, resource_id, ignore_response=False):
        return self.delete(table='bluetooths', pk=resource_id, ignore_response=ignore_response)

    def create_radio(self, radio):
        return self.post(table='radios', body=radio)

    def get_radio(self, radio_id):
        return self.get(table='radios', pk=radio_id)

    def update_radio(self, resource_id, resource):
        return self.put(table='radios', pk=resource_id, body=resource)

    def patch_radio(self, resource_id, resource):
        return self.patch(table='radios', pk=resource_id, body=resource)

    def delete_radio(self, resource_id, ignore_response=False):
        return self.delete(table='radios', pk=resource_id, ignore_response=ignore_response)

    # REST Helper methods

    def get(self, table, pk):
        response = self.client.get('{base}{resource}/1/'.format(base=BASE_URL, resource=table), kwargs={'pk': pk})
        self.assertEqual(response.status_code, 200)
        content = response.content
        model = json.loads(content)
        return model

    def post(self, table, body):
        response = self.client.post('{base}{resource}/'.format(base=BASE_URL, resource=table),
                                    body,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        return response

    def put(self, table, pk, body):
        response = self.client.put('{base}{resource}/{pk}/'.format(base=BASE_URL, resource=table, pk=pk),
                                   body,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return response

    def patch(self, table, pk, body):
        response = self.client.patch('{base}{resource}/{pk}/'.format(base=BASE_URL, resource=table, pk=pk),
                                     body,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return response

    def delete(self, table, pk, ignore_response=False):
        response = self.client.delete('/api/v1/{resource}/{pk}/'.format(base=BASE_URL, resource=table, pk=pk),
                                      content_type='application/json')
        if not ignore_response:
            self.assertEqual(response.status_code, 204)
        return response

    def is_date_newer(self, left, right):
        difference = iso8601.parse_date(right) - iso8601.parse_date(left)
        if difference.total_seconds() <= 0:
            print(iso8601.parse_date(right))
            print(iso8601.parse_date(left))
        self.assertGreaterEqual(difference.total_seconds(), 0)
