# -*- coding: utf-8 -*-

from django.db.models import Model


def parse_decimal_degree(degree):
    """
    Extracts a float decimal degree from a string.
    """

    from re import match as re_match

    return re_match(r'^[+\-]{0,1}[0-9]{1,3}\.[0-9]{1,8}$', degree).group(0)


def is_valid_longitude(longitude):
    from decimal import Decimal

    return (Decimal(longitude) >= Decimal('-180.0')) and (Decimal(longitude) <= Decimal('180.0'))


def is_valid_latitude(latitude):
    from decimal import Decimal

    return (Decimal(latitude) >= Decimal('-90.0')) and (Decimal(latitude) <= Decimal('90.0'))


def validate_latitude(latitude):
    from django.core.exceptions import ValidationError

    try:
        if is_valid_longitude(parse_decimal_degree(latitude)):
            return
    except Exception as exception:
        raise ValidationError('{0} is not a valid Decimal Degree latitude. '.format(str(latitude))) from exception


def validate_longitude(longitude):
    from django.core.exceptions import ValidationError

    try:
        if is_valid_longitude(parse_decimal_degree(longitude)):
            return
    except Exception as exception:
        raise ValidationError('{0} is not a valid Decimal Degree longitude. '.format(str(longitude))) from exception


class Contact(Model):
    """
    A contact person.
    """
    from django.db.models import CharField, EmailField, URLField

    email_address = EmailField(verbose_name='E-mail address')
    name = CharField(max_length=100, unique=False, verbose_name='Name')
    edupersonprincipalname = CharField(max_length=100, blank=True, null=True,
                                       verbose_name='eduPersonPrincipalName',
                                       unique=True)
    telephone_number = CharField(max_length=40, blank=True,
                                 verbose_name='Telephone number (E.123 international notation)')
    website_url = URLField(max_length=2000, blank=True, verbose_name='Website URL')

    def __unicode__(self):
        return '{name:s} <{email_address:s}>'.format(name=self.name, email_address=self.email_address)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('name',)
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'


class Consortium(Model):
    """
    A CLARIN consortium.
    """
    from django.db.models import BooleanField, CharField, URLField

    country_code = CharField(verbose_name='Country code', max_length=3, unique=True)
    country_name = CharField(verbose_name='Country name', max_length=20, unique=True)
    is_observer = BooleanField(verbose_name='Is observer (not member)?', default=False)
    name = CharField(verbose_name='Name', max_length=40, blank=True)
    website_url = URLField(verbose_name='Website URL', max_length=2000, blank=True)
    alias = CharField(verbose_name='DNS subdomain alias * (*.clarin.eu)', blank=True, max_length=25)

    def __unicode__(self):
        return '{name:s} ({country_code})'.format(name=self.name, country_code=self.country_code)

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
    from django.db.models import CharField

    type = CharField(verbose_name='Certified centre type', max_length=1, unique=True)

    def __unicode__(self):
        return '{type:s}'.format(type=self.type)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('type',)
        verbose_name = 'centre type'
        verbose_name_plural = 'centre types'


class Centre(Model):
    """
    A CLARIN centre.
    """
    from django.db.models import BooleanField, CharField, ManyToManyField, ForeignKey, URLField

    name = CharField(verbose_name='Name', max_length=200, unique=True)
    shorthand = CharField(verbose_name='Shorthand code', max_length=30, unique=True)
    organisation_name = CharField(verbose_name='Organisation', max_length=100)
    institution = CharField(verbose_name='Institution', max_length=200)
    working_unit = CharField(verbose_name='Working unit', max_length=200)
    address = CharField(verbose_name='Address', max_length=100)
    postal_code = CharField(verbose_name='Postal code', max_length=20)
    city = CharField(verbose_name='City', max_length=100)
    latitude = CharField(verbose_name='Latitude (from e.g. Google Maps)', validators=[validate_latitude],
                         max_length=20)
    longitude = CharField(verbose_name='Longitude (from e.g. Google Maps)', validators=[validate_longitude],
                          max_length=20)

    type = ManyToManyField(to=CentreType, verbose_name='Type')
    type_status = CharField(verbose_name="Comments about centre's type", max_length=100, blank=True)
    administrative_contact = ForeignKey(Contact, related_name='administrative_contact')
    technical_contact = ForeignKey(Contact, related_name='technical_contact')
    monitoring_contacts = ManyToManyField(to=Contact, related_name='monitoring_contacts', blank=True)
    website_url = URLField(verbose_name='Website URL', max_length=2000)
    description = CharField(verbose_name='Description', max_length=500, blank=True)
    expertise = CharField(verbose_name='Expertise', max_length=200, blank=True)
    consortium = ForeignKey(Consortium, blank=True, null=True)

    type_certificate_url = URLField(verbose_name='Centre type certificate URL', max_length=2000, blank=True)
    dsa_url = URLField(verbose_name='Data Seal of Approval URL', max_length=2000, blank=True)
    pid_status = CharField(verbose_name='Persistent Identifier usage status', max_length=200, blank=True)
    long_term_archiving_policy = CharField(verbose_name='Long Time Archiving Policy', max_length=200, blank=True)
    repository_system = CharField(verbose_name='Repository system', max_length=200, blank=True)
    strict_versioning = BooleanField(verbose_name='Strict versioning?', default=False)

    def __unicode__(self):
        return '{shorthand:s} ({city:s})'.format(shorthand=self.shorthand, city=self.city)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('shorthand',)
        verbose_name = 'centre'
        verbose_name_plural = 'centres'


class MetadataFormat(Model):
    """
    A metadata format as per OAI-PMH ( http://www.openarchives.org/OAI/openarchivesprotocol.html#ListMetadataFormats ).
    Deprecated, use ListMetadataFormats verb on endpoint instead.
    """
    from django.db.models import CharField

    name = CharField(verbose_name='Metadata format name', max_length=30, unique=True)

    def __unicode__(self):
        return '{name:s}'.format(name=self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('name',)
        verbose_name = 'metadata format'
        verbose_name_plural = 'metadata formats'


class URLReference(Model):
    """
    A web reference (URL) with description.
    """
    from django.db.models import CharField, ForeignKey, URLField

    centre = ForeignKey(Centre)
    description = CharField(verbose_name='Content description', max_length=300)
    url = URLField(verbose_name='URL', max_length=2000, unique=True)

    def __unicode__(self):
        return '{url:s} ({centre_shorthand:s})'.format(url=self.url, centre_shorthand=self.centre.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('url',)
        verbose_name = "URL reference"
        verbose_name_plural = "URL references"


class OAIPMHEndpoint(Model):
    """
    An OAI-PMH Endpoint.
    """
    from django.db.models import CharField, ForeignKey, URLField

    centre = ForeignKey(Centre)
    metadata_format = ForeignKey(MetadataFormat, verbose_name='Metadata format (historic artifact)')
    # TODO: fix old API's XSD to allow more MetadataFormats
    web_services_set = CharField(verbose_name='Web services set (historic artifact)', max_length=100, blank=True)
    web_services_type = CharField(verbose_name='Web services type (historic artifact)',
                                  choices=(('REST', 'REST'), ('SOAP', 'SOAP'), ('WebLicht', 'WebLicht')),
                                  default='REST',
                                  max_length=8)
    uri = URLField(verbose_name='Base URI', max_length=2000, unique=True)

    def __unicode__(self):
        return '{uri:s} ({centre_shorthand:s})'.format(uri=self.uri, centre_shorthand=self.centre.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('uri',)
        verbose_name = "OAI-PMH endpoint"
        verbose_name_plural = "OAI-PMH endpoints"


class FCSEndpoint(Model):
    """
    A CLARIN FCS Endpoint.
    """
    from django.db.models import ForeignKey, URLField

    centre = ForeignKey(Centre)
    uri = URLField(verbose_name='Base URI', max_length=2000, unique=True)

    def __unicode__(self):
        return '{uri:s} ({centre_shorthand:s})'.format(uri=self.uri, centre_shorthand=self.centre.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('uri',)
        verbose_name = 'FCS endpoint'
        verbose_name_plural = 'FCS endpoints'


class SAMLServiceProvider(Model):
    """
    A CLARIN SPF SAML Service Provider.
    """
    from django.db.models import BooleanField, CharField, ForeignKey, URLField

    entity_id = CharField(verbose_name='Entity ID', max_length=1024, unique=True)
    centre = ForeignKey(Centre)
    status_url = URLField(verbose_name='Status URL', max_length=1024, blank=True)
    production_status = BooleanField(verbose_name='Has production status?', default=True)

    def __unicode__(self):
        return '{entity_id:s} ({centre_shorthand:s})'.format(entity_id=self.entity_id,
                                                             centre_shorthand=self.centre.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('entity_id',)
        verbose_name = 'SAML Service Provider'
        verbose_name_plural = 'SAML Service Providers'


class SAMLIdentityFederation(Model):
    """
    A SAML identity federation.
    """
    from django.db.models import CharField, TextField, URLField

    shorthand = CharField(verbose_name='Shorthand code', max_length=30, unique=True)
    information_url = URLField(verbose_name='Information URL', max_length=1024)
    saml_metadata_url = URLField(verbose_name='SAML metadata URL', max_length=1024)
    signing_key = TextField(verbose_name='XML digital signature X.509v3 public key (PEM format, without '
                                         '"-----BEGIN CERTIFICATE-----" begin and and end marker)', blank=True)

    def __unicode__(self):
        return '{shorthand:s}'.format(shorthand=self.shorthand)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('shorthand',)
        verbose_name = 'SAML identity federation'
        verbose_name_plural = 'SAML identity federations'