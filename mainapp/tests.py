# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.test import TestCase
from django.utils import timezone as dj_timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from mainapp.models import Client
from mainapp.views import DistributionViewSet, ClientViewSet


class DistributionClientTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client.objects.create(email='testuser@test.ru', password='testpass1')
        self.admin = Client.objects.create_superuser(email='adminuser@test.ru', password='?Adminpass12345')

    def test_post_client(self):
        request = self.factory.post('/api/client/', data=dict(email='testuser2@test.ru', password='testpass2'))
        force_authenticate(request, user=self.admin)
        response = ClientViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_distribution(self):
        date_from = dj_timezone.now() - datetime.timedelta(minutes=10)
        date_to = dj_timezone.now() + datetime.timedelta(days=1)

        request = self.factory.get('/api/client/')
        force_authenticate(request, user=self.admin)
        response = ClientViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        request = self.factory.post('/api/distribution/',  data={"started_at": date_from,
                                                                  "finished_at": date_to,
                                                                  "property_filter": "mail"})
        force_authenticate(request, user=self.admin)
        response = DistributionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
