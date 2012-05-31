#!/usr/bin/env python

from django.conf import settings
from django.test import TransactionTestCase
from django.test.client import Client
from django.utils import simplejson as json

from panda.models import SearchSubscription, UserProxy 
from panda.tests import utils

class TestAPISearchSubscriptions(TransactionTestCase):
    fixtures = ['init_panda.json']

    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        
        utils.setup_test_solr()
        
        self.user = utils.get_panda_user()
        self.dataset = utils.get_test_dataset(self.user)
        self.upload = utils.get_test_data_upload(self.user, self.dataset)

        self.dataset.import_data(self.user, self.upload, 0)

        self.auth_headers = utils.get_auth_headers()

        self.client = Client()

    def test_get(self):
        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.get('/api/1.0/search_subscription/%i/' % sub.id, **self.auth_headers) 

        self.assertEqual(response.status_code, 200)

    def test_get_not_user(self):
        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.get('/api/1.0/search_subscription/%i/' % sub.id) 

        self.assertEqual(response.status_code, 401)

    def test_get_unauthorized(self):
        UserProxy.objects.create_user('nobody@nobody.com', 'nobody@nobody.com', 'password')

        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.get('/api/1.0/search_subscription/%i/' % sub.id, **utils.get_auth_headers('nobody@nobody.com')) 

        self.assertEqual(response.status_code, 404)

    def test_list(self):
        SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.get('/api/1.0/search_subscription/', data={ 'limit': 5 }, **self.auth_headers)

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.content)

        self.assertEqual(len(body['objects']), 1)
        self.assertEqual(body['meta']['total_count'], 1)
        self.assertEqual(body['meta']['limit'], 5)
        self.assertEqual(body['meta']['offset'], 0)
        self.assertEqual(body['meta']['next'], None)
        self.assertEqual(body['meta']['previous'], None)

    def test_list_unauthorized(self):
        UserProxy.objects.create_user('nobody@nobody.com', 'nobody@nobody.com', 'password')

        response = self.client.get('/api/1.0/search_subscription/', data={ 'limit': 5 }, **utils.get_auth_headers('nobody@nobody.com')) 

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.content)

        self.assertEqual(len(body['objects']), 0)
        self.assertEqual(body['meta']['total_count'], 0)
        self.assertEqual(body['meta']['limit'], 5)
        self.assertEqual(body['meta']['offset'], 0)
        self.assertEqual(body['meta']['next'], None)
        self.assertEqual(body['meta']['previous'], None)

    def test_update(self):
        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.put('/api/1.0/search_subscription/%i/' % sub.id, data=json.dumps({}), content_type='application/json', **self.auth_headers) 

        self.assertEqual(response.status_code, 405)

    def test_update_unauthorized(self):
        UserProxy.objects.create_user('nobody@nobody.com', 'nobody@nobody.com', 'password')

        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.put('/api/1.0/search_subscription/%i/' % sub.id, data=json.dumps({}), content_type='application/json', **utils.get_auth_headers('nobody@nobody.com')) 
        # This returns 201 (rather than 401), because the PUT fails to match an
        # existing subscription that the user has access to and thus falls
        # back to creating a new one.
        # This is probably not ideal, but works.
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.delete('/api/1.0/search_subscription/%i/' % sub.id, **self.auth_headers)

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/1.0/search_subscription/%i/' % sub.id, **self.auth_headers)

        self.assertEqual(response.status_code, 404)

        with self.assertRaises(SearchSubscription.DoesNotExist):
            SearchSubscription.objects.get(id=sub.id)

    def test_delete_unauthorized(self):
        UserProxy.objects.create_user('nobody@nobody.com', 'nobody@nobody.com', 'password')

        sub = SearchSubscription.objects.create(
            user=self.user,
            dataset=self.dataset,
            query='*'
        )

        response = self.client.delete('/api/1.0/search_subscription/%i/' % sub.id, **utils.get_auth_headers('nobody@nobody.com'))

        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/1.0/search_subscription/%i/' % sub.id, **self.auth_headers)

        self.assertEqual(response.status_code, 200)

        # Verify no exception is raised
        SearchSubscription.objects.get(id=sub.id)

