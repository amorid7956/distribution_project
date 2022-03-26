from rest_framework import serializers
from rest_framework import exceptions
from django.utils import timezone as dj_timezone

from .models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = ['id', 'started_at', 'finished_at', 'property_filter']

    def validate(self, attrs):
        finished_datetime = attrs.get('finished_at', '')
        if finished_datetime != '':
            if finished_datetime < dj_timezone.now():
                raise exceptions.ValidationError('Finished datetime for distribution has expired!')
        return attrs

