# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from drf_yasg.inspectors import SwaggerAutoSchema

from .models import Client, Distribution
from .serializers import ClientSerializer, DistributionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    swagger_schema = SwaggerAutoSchema
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        return ClientSerializer


class DistributionViewSet(viewsets.ModelViewSet):
    swagger_schema = SwaggerAutoSchema
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Distribution.objects.all()

    def get_serializer_class(self):
        return DistributionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distribution = serializer.save()
        distribution.send_mails_for_current_distribution()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
