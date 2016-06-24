from rest_framework import serializers
from md import models as stops


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = stops.Agency
        fields = ('id', 'name')
