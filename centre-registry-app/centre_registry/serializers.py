from rest_framework import serializers
from django_countries.serializer_fields import CountryField


from centre_registry.models import AssessmentDates
from centre_registry.models import Centre
from centre_registry.models import CentreType
from centre_registry.models import Contact
from centre_registry.models import Consortium
# from centre_registry.models import FCSEndpoint
# from contre_registry.models import OAIPMHEndpoint
from centre_registry.models import Organisation
# from centre_registry.models import URLReference


class CentreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentreType
        fields = ['type']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ConsortiumSerializer(serializers.ModelSerializer):
    country = CountryField()
    class Meta:
        model = Consortium
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class AssessmentDatesSerializer(serializers.ModelSerializer):
    type = CentreTypeSerializer(many=True)

    class Meta:
        model = AssessmentDates
        exclude = ['id']


class CentreSerializer(serializers.ModelSerializer):
    country = CountryField()
    type = CentreTypeSerializer(many=True)
    technical_contact = ContactSerializer()
    administrative_contact = ContactSerializer()
    monitoring_contacts = ContactSerializer(many=True)
    consortium = ConsortiumSerializer()
    organisation_fk = OrganisationSerializer()
    assessmentdates = AssessmentDatesSerializer(many=True)
    class Meta:
        model = Centre
        fields = '__all__'


# class OAIPMHEndpointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OAIPMHEndpoint
#         fields = '__all__'
#
# class FCSEndpointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FCSEndpoint
#         fields = '__all__'
#
# class URLReferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = URLReference
#         fields = '__all__'
