[![Travis Status](https://travis-ci.org/clarin-eric/Centre-Registry.svg?branch=sauce-ci)](https://travis-ci.org/clarin-eric/Centre-Registry)
[![Sauce Test Status](https://saucelabs.com/buildstatus/centre-registry)](https://app.saucelabs.com/u/centre-registry)
# The Centre Registry
The Centre Registry is a Django web application and service that serves as administrative registry for CLARIN, documented on [the CLARIN Trac](https://trac.clarin.eu/wiki/Centre%20Registry).

## REST API
`api/KML/`
Gives a KML file (Keyhole Markup) with geographical information about all Centres, for use in
mapping applications.

`api/KML/[N[N[N[N[N[N]]]]]`.
Gives a KML file (Keyhole Markup) with geographical information about Centres of any type N, for
use in mapping applications. For example: `api/KML/EBC`

`api/model/M`, where M is one of the models in the administration interface `CentreType`,
`Centre`, `Contact`, `Consortium`, `FCSEndpoint`, `URLReference`, `MetadataFormat`,
`OAIPMHEndpoint`, `SAMLIdentityFederation`, `SAMLServiceProvider`:
Gives a JSON representation of all data belonging to that model in the database.

## XML API
`restxml/`: gives a list of centres including the centre ID in XML.

`restxml/n`, where n is a centre ID: Gives detailed information about a centre in XML that is validated with this schema: ​http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1320657629667/xsd

### Notes on XML API
Some services (WebLicht?) may depend on optional string-type properties of OAI-PMH endpoints that have been exported since the first API versions:

    `WebServiceType` is the semantic indication of the kind of webservices offered.
    `WebServicesSet` is just a name for the OAI-PMH set that contains the relevant web service metadata descriptions. It could be anything, so a harvester should be able to deal with arbitrary set names. 

## Development
### Make migrations
Django wants to detect modifications made to the data model of apps:
```sh
'Centre-Registry-config/manage.py' makemigrations
```
When you change an existing field, be careful to only change one property per `makemigrations` run (e.g, first change the field identifier, then the  `verbose_name` string).

### Show migrations
To show migrations previously made, and whether they have been carried out or not:
```sh
'Centre-Registry-config/manage.py' showmigrations
```

### Migrate
After making migrations, you will still need to apply them:
```sh
'Centre-Registry-config/manage.py' migrate
```
**Always generate new a fixture after migrating.** If you do not, your fixture will not correspond to the actual data model, and testing runs will fail outright.

### Generate fixtures
For testing, you will need a sample of the data that obeys the data model. To generate such a *fixture*, run this:
```sh
'Centre-Registry-config/manage.py' dumpdata \
    --format=json --indent 4 \
    --natural-primary --natural-foreign \
    --exclude=auth --exclude=sessions --exclude=admin --exclude=contenttypes \
    --no-color --traceback -o \
    'centre-registry-app/centre_registry/fixtures/test_data.json'
```
When you change an existing field of some class in your data model, be careful to make only this single change per `makemigrations` run (e.g, first change the field identifier, then the  `verbose_name` value), otherwise `makemigrations` will go awry.

### Test
#### From an IDE
Within your IDE such as IntelliJ IDEA, your project should have a Django 'facet' detected automatically. If so, you should have the complete testing 'run configuration' available.
#### From the command line
First make sure that `centre-registry-app` and `Centre-Registry-config` are installed. Then run the test modules `centre_registry.test_api` and `centre_registry.test_ui` like so:
```sh
'Centre-Registry-config/manage.py' test centre_registry
```
Or more selectively:
```sh
'Centre-Registry-config/manage.py' test centre_registry.{test_api,test_ui}
```

# Continuous Integration

The API and the UI are both tested by the continuous integration system.

After each commit (or PR), Travis CI will:
- build the project.
- execute the API tests.
- connect to Sauce Labs and run the UI (Selenium-based) tests targeting multiple browsers.

Current overall status of Travis build and tests:
[![Travis Status](https://travis-ci.org/clarin-eric/Centre-Registry.svg?branch=sauce-ci)](https://travis-ci.org/clarin-eric/Centre-Registry)

In the last stage of the build and test process, the continuous integration system will run all UI tests for multiple browser and operating system combinations.

Current status of UI tests:
[![Sauce Test Status](https://saucelabs.com/buildstatus/centre-registry)](https://app.saucelabs.com/u/centre-registry)

Test results breakdown per browser and operating system:

[![Build Status](https://app.saucelabs.com/browser-matrix/centre-registry.svg)](https://saucelabs.com/u/centre-registry)

#### Big Thanks

Automated cross-browser testing platform and open source ❤️ provided by [Sauce Labs][homepage]

[homepage]: https://saucelabs.com
