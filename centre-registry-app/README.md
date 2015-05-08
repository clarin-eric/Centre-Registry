# The Centre Registry
The Centre Registry is a Django web application and service that serves as administrative registry for CLARIN, documented on [the CLARIN Trac](https://trac.clarin.eu/wiki/Centre%20Registry).

## Prepare
Activate the virtual environment for the Centre Registry. Set the following environment variables properly, which should work for you as long as your current directory is `/srv/apps/{staging,production}`. `cd` to one of those directories in order for the rest of this documentation to work as well.

```sh
PYTHONPATH='centre-registry-app/:centre-registry-config/' export PYTHONPATH ; 
DJANGO_SETTINGS_MODULE='centre_registry_project.release_staging_settings' export DJANGO_SETTINGS_MODULE ; 
```

## Install
You will need the private configuration `centre-registry-config` package and this package. The application and configuration are deployed under `/srv/apps/{staging,production}`. 

 1. SSH-login as `python` to the `centres-clarin` host as instructed
    elsewhere and issue `tmux attach`.  
 2. Press Ctrl-B W and select the correct window with your keyboard arrows and ⏎ (staging, vs. production).
 3. The web application server is at the foreground. Press Ctrl-C to stop    the server orderly.
 4. Optional: update marginal virtual environment packages. *
 5. The following commands will uninstall and reinstall the Centre Registry application and configuration:

```sh
 # Which version to install: 
version='2.3'
 # Only necessary if switching from directory based 'editable' install to distribution: 
pip uninstall 'centre-registry-app' && 

pip --cert='/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem' \
    install --upgrade "centre_registry_app-$cr_version.tar.gz" 

tar -xvf "centre_registry_config-$cr_version.tar.gz" && 
ln -fvs "centre_registry_config-$cr_version/" 'centre-registry-config' &&
pip install -e "centre_registry_config-$cr_version/" ; 
```

### * Optional: update marginal virtual environment packages
```bash
pip --cert='/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem' \
    install --upgrade setuptools &&

pip --cert='/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem' \
    install --upgrade pip &&

pip --cert='/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem' \
    install --upgrade uWSGI gunicorn && 
```

## Configure
The configuration package `centre-registry-config` stores and rotates logs in `'/var/log/Centre_Registry/'`. 
The files 
`'centre-registry-config/centre_registry_project/{development,production,staging}.{ini,py}'` are the main configuration files for development, production and staging deployment types. The `*.py` files are the Django settings files for the application as deployed.  The `*.ini` files are settings files for the web application server uWSGI.

## Run
### Development using the Django web server on your local computer
It is advisable to use the web server embedded in Django in order to have debugging support in your IDE, such as IntelliJ IDEA.
```
python 'centre-registry-config/manage.py' runserver
```

### Run with web application server
To use a web application server for e.g. the staging deployment, such as uWSGI: 
```
sudo uwsgi 'centre-registry-config/centre_registry_project/staging.ini' 
```
**Don't run development settings on a server.** The development settings will have Django output debugging information (sometimes sensitive information) onto the user's view to anyone who can connect to it.

## Development
### Make migrations
Django wants to detect modifications made to the data model of apps: 
```sh
'centre-registry-config/manage.py' makemigrations
```
When you change an existing field, be careful to only change one property per `makemigrations` run (e.g, first change the field identifier, then the  `verbose_name` string). 

### Show migrations
To show migrations previously made, and whether they have been carried out or not: 
```sh
'centre-registry-config/manage.py' showmigrations
```
### Generate fixtures
For testing, you will need a sample of the data that obeys the data model. To generate such a *fixture*, run this: 
```sh
'centre-registry-config/manage.py' dumpdata \
    --format=json --indent 4 \
    --natural-primary --natural-foreign \
    --exclude=auth --exclude=sessions --exclude=admin --exclude=contenttypes  --exclude=auth \
    --no-color --traceback -o \
    'centre-registry-app/centre_registry/fixtures/test_data.json'
```
When you change an existing field of some class in your data model, be careful to make only this single change per `makemigrations` run (e.g, first change the field identifier, then the  `verbose_name` value), otherwise `makemigrations` will go awry.

### Migrate
After making migrations, you will still need to apply them:
```sh
'centre-registry-config/manage.py' migrate
```
**Always generate new a fixture after migrating.** If you do not, your fixture will not correspond to the actual data model, and testing runs will fail outright.

### Test
#### From an IDE
Within your IDE such as IntelliJ IDEA, your project should have a Django 'facet' detected automatically. If so, you should have the complete testing 'run configuration' available.
#### From the command line
First make sure that `centre-registry-app` and `centre-registry-config` are installed. Then run the test modules `centre_registry.test_api` and `centre_registry.test_ui` like so:
```sh
'centre-registry-config/manage.py' test centre_registry
```
Or more selectively:
```sh
'centre-registry-config/manage.py' test centre_registry.{test_api,test_ui}
```