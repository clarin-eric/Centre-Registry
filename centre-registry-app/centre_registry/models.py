from decimal import Decimal
from re import match as re_match

from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import TextField
from django.db.models import URLField
from django.db.models import DateField
from django.db.models import CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET, DO_NOTHING


def parse_decimal_degree(degree):
    """
    Extracts a float decimal degree from a string.
    """
    return re_match(r'^[+\-]{0,1}[0-9]{1,3}\.[0-9]{1,8}$', degree).group(0)


def is_valid_longitude(longitude):
    return (Decimal(longitude) >= Decimal('-180.0')) and (
        Decimal(longitude) <= Decimal('180.0'))


def is_valid_latitude(latitude):
    return (Decimal(latitude) >= Decimal('-90.0')) and (
        Decimal(latitude) <= Decimal('90.0'))


def validate_latitude(latitude):
    try:
        if is_valid_longitude(parse_decimal_degree(latitude)):
            return
    except Exception as exception:
        raise ValidationError(
            '{0} is not a valid Decimal Degree latitude. '.format(
                str(latitude))) from exception


def validate_longitude(longitude):
    try:
        if is_valid_longitude(parse_decimal_degree(longitude)):
            return
    except Exception as exception:import ast


class Contact(Model):
    """
    A contact person.
    """
    email_address = EmailField(verbose_name='E-mail address')
    name = CharField(max_length=100, unique=False, verbose_name='Name')
    edupersonprincipalname = CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='eduPersonPrincipalName',
        unique=True)
    telephone_number = CharField(
        max_length=40,
        blank=True,
        verbose_name='Telephone number (E.123 international notation)')
    website_url = URLField(
        max_length=2000, blank=True, verbose_name='Website URL')

    def __unicode__(self):
        return '{name:s} <{email_address:s}>'.format(
            name=self.name, email_address=self.email_address)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('name', )
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'


class Consortium(Model):
    """
    A CLARIN consortium.
    """
    country_code = CharField(
        verbose_name='Country code', max_length=3, unique=True)
    country_name = CharField(
        verbose_name='Country name', max_length=20, unique=True)
    is_observer = BooleanField(
        verbose_name='Is observer (not member)?', default=False)
    name = CharField(verbose_name='Name', max_length=40, blank=True)
    website_url = URLField(
        verbose_name='Website URL', max_length=2000, blank=True)
    alias = CharField(
        verbose_name='DNS subdomain alias * (*.clarin.eu)',
        blank=True,
        max_length=25)

    def __unicode__(self):
        return '{name:s} ({country_code})'.format(
            name=self.name, country_code=self.country_code)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('country_code', 'country_name', 'name')
        verbose_name = 'consortium'
        verbose_name_plural = 'consortia'


class CentreType(Model):
    """
    A CLARIN centre type
    """
    type = CharField(
        verbose_name='Certified centre type', max_length=1, unique=True)

    def __unicode__(self):
        return '{type:s}'.format(type=self.type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('type', )
        verbose_name = 'centre type'
        verbose_name_plural = 'centre types'


class AssessmentDates(Model):
    """
    Assessment due date
    """
    issuedate = DateField(verbose_name='Assessment issued date (YYYY-MM-DD)')
    duedate = DateField(verbose_name='Assessment due date (YYYY-MM-DD)')
    type = ManyToManyField(to=CentreType, verbose_name='Type')

    def __unicode__(self):
        types = u", ".join([x.type for x in self.type.all()])
        return u'[{0}] valid till [{1}] for {2}'.format(
            self.issuedate, self.duedate, types
        )

    def __str__(self):
        return self.__unicode__()

    @property
    def brief(self):
        types = u", ".join([x.type for x in self.type.all()])
        return u'{0} valid till {1} for [{2}]'.format(
            self.issuedate, self.duedate, types
        )

    class Meta:
        ordering = ('issuedate', 'duedate')
        verbose_name = 'issue/due dates for a centre administrative_contacttype'
        verbose_name_plural = 'issue/due dates for a centre type'


class Organisation(Model):
    organisation_name = CharField(verbose_name='Organisation', max_length=100, blank=False)
    institution = CharField(verbose_name='Institution', max_length=200, blank=True)
    working_unit = CharField(verbose_name='Working unit', max_length=200, blank=True)
    address = CharField(verbose_name='Address', max_length=100)
    postal_code = CharField(verbose_name='Postal code', max_length=20)
    city = CharField(verbose_name='City', max_length=100)
    latitude = CharField(
        verbose_name='Latitude (from e.g. Google Maps)',
        validators=[validate_latitude],
        max_length=20)
    longitude = CharField(
        verbose_name='Longitude (from e.g. Google Maps)',
        validators=[validate_longitude],
        max_length=20)

    def __unicode__(self):
        return '{organisation_name:s} {institution:s} {working_unit:s}'.format(
            organisation_name=self.organisation_name, institution=self.institution, working_unit=self.working_unit)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('organisation_name', )
        verbose_name = 'organisation'
        verbose_name_plural = 'organisations'


class Centre(Model):
    """
    A CLARIN centre.
    """
    name = CharField(verbose_name='Name', max_length=200, unique=True)
    shorthand = CharField(
        verbose_name='Shorthand code', max_length=30, unique=True)
    organisation_fk = ForeignKey(Organisation, on_delete=CASCADE, blank=True, null=True)

    type = ManyToManyField(to=CentreType, verbose_name='Type')
    type_status = CharField(
        verbose_name="Comments about centre's type",
        max_length=100,
        blank=True)
    assessmentdates = ManyToManyField(
        to=AssessmentDates, related_name='assessmentdates', blank=True
    )

    administrative_contact = ForeignKey(
        Contact, related_name='administrative_contact', on_delete=PROTECT)
    technical_contact = ForeignKey(Contact, related_name='technical_contact', on_delete=PROTECT)
    monitoring_contacts = ManyToManyField(
        to=Contact, related_name='monitoring_contacts', blank=True)
    website_url = URLField(verbose_name='Website URL', max_length=2000)
    description = CharField(
        verbose_name='Description', max_length=500, blank=True)
    expertise = CharField(verbose_name='Expertise', max_length=200, blank=True)
    consortium = ForeignKey(Consortium, blank=True, null=True, on_delete=SET_NULL)

    type_certificate_url = URLField(
        verbose_name='Centre type certificate URL',
        max_length=2000,
        blank=True)
    dsa_url = URLField(
        verbose_name='Data Seal of Approval URL', max_length=2000, blank=True)
    pid_status = CharField(
        verbose_name='Persistent Identifier usage status',
        max_length=200,
        blank=True)
    long_term_archiving_policy = CharField(
        verbose_name='Long Time Archiving Policy', max_length=200, blank=True)
    repository_system = CharField(
        verbose_name='Repository system', max_length=200, blank=True)
    strict_versioning = BooleanField(
        verbose_name='Strict versioning?', default=False)

    def __unicode__(self):
        return '{shorthand:s} ({city:s})'.format(
            shorthand=self.shorthand, city=getattr(self.organisation_fk, 'city'))

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('shorthand', )
        verbose_name = 'centre'
        verbose_name_plural = 'centres'


# class KCentre(Model):
#     centre = ForeignKey(Centre, related_name='centre')
#       name = CharField(verbose_name='Name', max_length=200, unique=True)
#       shorthand = CharField(verbose_name='Shorthand code', max_length=30, unique=True)
#     class Meta:
#         verbose_name = 'k-centre'
#         verbose_name_plural = 'k-centres'


class URLReference(Model):
    """
    A web refereweb_servicence (URL) with description.
    """

    centre = ForeignKey(Centre, on_delete=CASCADE)
    description = CharField(verbose_name='Content description', max_length=300)
    url = URLField(verbose_name='URL', max_length=2000, unique=True)

    def __unicode__(self):
        return '{url:s} ({centre_shorthand:s})'.format(
            url=self.url, centre_shorthand=self.centre.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('url', )
        verbose_name = "URL reference"
        verbose_name_plural = "URL references"


class OAIPMHEndpointSet(Model):
    #TODO rename web_service field name
    set_spec = CharField(verbose_name='Set specification', blank=True, max_length=1024)
    set_type = CharField(verbose_name='Set type', max_length=1024, default='VLO')

    def __unicode__(self):
        if self.set_spec == '':
            return '{set_spec:s} ({set_type:s})'.format(
                set_spec='No spec', set_type=self.set_type)
        else:
            return '{set_spec:s} ({set_type:s})'.format(
                set_spec=self.set_spec, set_type=self.set_type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('set_spec', 'set_type')
        verbose_name = "OAI-PMH Set"
        verbose_name_plural = "OAI-PMH Sets"


class OAIPMHEndpoint(Model):
    """
    An OAI-PMH Endpoint.
    """
    centre = ForeignKey(Centre, blank=True, null=True, on_delete=CASCADE)
    uri = URLField(verbose_name='Base URI', max_length=2000, unique=True)
    note = CharField(verbose_name='Additional note', max_length=1024, blank=True)
    oai_pmh_sets = ManyToManyField(to=OAIPMHEndpointSet, blank=True, related_name="web_services")

    def __unicode__(self):
        return '{uri:s}'.format(
            uri=self.uri)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('uri', )
        verbose_name = "OAI-PMH Endpoint"
        verbose_name_plural = "OAI-PMH Endpoints"


class FCSEndpoint(Model):
    """
    A CLARIN FCS Endpoint.
    """
    centre = ForeignKey(Centre, blank=True, null=True, on_delete=SET_NULL)
    uri = URLField(verbose_name='Base URI', max_length=2000, unique=True)
    note = CharField(verbose_name='Additional note', max_length=1024, blank=True)

    def __unicode__(self):
        if self.centre is not None:
            return '{uri:s} ({centre_shorthand:s})'.format(
                uri=self.uri, centre_shorthand=self.centre.shorthand)
        else:
            return '{uri:s} ({centre_shorthand:s})'.format(
                uri=self.uri, centre_shorthand='NoCentre')

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('uri', )
        verbose_name = 'FCS endpoint'
        verbose_name_plural = 'FCS endpoints'


class SAMLServiceProvider(Model):
    """
    A CLARIN SPF SAML Service Provider.
    """
    entity_id = CharField(
        verbose_name='Entity ID', max_length=1024, unique=True)
    centre = ForeignKey(Centre, null=True, blank=True, on_delete=SET_NULL)
    status_url = URLField(
        verbose_name='Status URL', max_length=1024, blank=True)
    production_status = BooleanField(
        verbose_name='Has production status?', default=True)
    note = CharField(verbose_name='Additional note', max_length=1024, blank=True)

    def __unicode__(self):
        if self.centre is not None:
            return '{entity_id:s} ({centre_shorthand:s})'.format(
                entity_id=self.entity_id, centre_shorthand=self.centre.shorthand)
        else:
            return '{entity_id:s} ({centre_shorthand:s})'.format(
                entity_id=self.entity_id, centre_shorthand='NoCentre')

    def __str__(self): 
        return self.__unicode__()

    class Meta:
        ordering = ('entity_id', )
        verbose_name = 'SAML Service Provider'
        verbose_name_plural = 'SAML Service Providers'


class SAMLIdentityFederation(Model):
    """
    A SAML identity federation.
    """
    shorthand = CharField(
        verbose_name='Shorthand code', max_length=30, unique=True)
    information_url = URLField(verbose_name='Information URL', max_length=1024)
    saml_metadata_url = URLField(
        verbose_name='SAML metadata URL', max_length=1024)
    signing_key = TextField(
        verbose_name='XML digital signature X.509v3 public key (PEM format, '
        'without '
        '"-----BEGIN CERTIFICATE-----" begin and and end marker)',
        blank=True)

    def __unicode__(self):
        return '{shorthand:s}'.format(shorthand=self.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('shorthand', )
        verbose_name = 'SAML identity federation'
        verbose_name_plural = 'SAML identity federations'


