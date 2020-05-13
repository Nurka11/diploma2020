from rest_framework import serializers
from .models import CompetitorProduct


class PrefixSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitorProduct
        fields = ['id', 'name']
