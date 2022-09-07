import json
from deepdiff import DeepDiff
from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime

import iso8601
import datetime

BASE_URL = '/api/v2/'


class RestHelper:

    def __init__(self, client, assertEqual):
        self.client = client
        self.assertEqual = assertEqual

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
        if difference.total_seconds() < 0:
            print(iso8601.parse_date(right))
            print(iso8601.parse_date(left))
        self.assertGreater(difference.total_seconds(), 0)
