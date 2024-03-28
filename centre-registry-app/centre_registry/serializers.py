from rest_framework import serializers

from centre_registry.models import Centre
from centre_registry.models import CentreType
from centre_registry.models import Contact
from centre_registry.models import Consortium
from centre_registry.models import Organisation


class CentreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentreType
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ConsortiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consortium
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


class CentreSerializer(serializers.ModelSerializer):
    type = CentreTypeSerializer(many=True)
    technical_contact = ContactSerializer()
    administrative_contact = ContactSerializer()
    monitoring_contacts = ContactSerializer(many=True)
    consortium = ConsortiumSerializer()
    organisation_fk = OrganisationSerializer()

    class Meta:
        model = Centre
        fields = '__all__'
