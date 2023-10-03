from os import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
import http.client
import base64

try:
    import json
except ImportError:
    import simplejson as json

is_ci = (environ.get('TRAVIS') or '').lower() == 'true'


def set_test_status(jobid, passed=True):
    base64string = str(base64.b64encode(bytes('%s:%s' % (environ["SAUCE_USERNAME"], environ["SAUCE_ACCESS_KEY"]),'utf-8')))[1:]
    body_content = json.dumps({"passed": passed})
    connection = http.client.HTTPSConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (environ["SAUCE_USERNAME"], jobid),
                       body_content,
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200


class SystemTestCase(StaticLiveServerTestCase):
    fixtures = ['test_data.json']
    port = 9999

    @classmethod
    def setUpClass(self):
        # TODO: Replace Travis CI & Sauce Labs with generic testing code.
        if is_ci:
            hub_url = ("{username:s}:{access_key:s}@ondemand.us-west-1.saucelabs.com"
                .format(
                username=environ["SAUCE_USERNAME"],
                access_key=environ["SAUCE_ACCESS_KEY"]))

            match environ["browserName"]:
                case "firefox":
                    options = FirefoxOptions();
                case "chrome":
                    options = ChromeOptions();
                case "MicrosoftEdge":
                    options = EdgeOptions();
                case "safari":
                    options = SafariOptions();

            options.browser_version = environ["browserVersion"]
            options.platform_name = environ["platformName"]
            options.headless = True

            sauce_options = {
                "name": "centre-registry_" + environ["TRAVIS_JOB_NUMBER"],
                "build": environ["TRAVIS_BUILD_NUMBER"],
                "tags": [environ["TRAVIS_PYTHON_VERSION"], "CI"],
                "tunnelName": environ["TRAVIS_JOB_NUMBER"]   
            }
            options.set_capability('sauce:options', sauce_options)
            self.selenium = Remote(command_executor="https://{hub_url:s}/wd/hub"
                    .format(hub_url=hub_url), options=options)
        else:
            self.selenium = webdriver.Firefox()
        super(SystemTestCase, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        super(SystemTestCase, self).tearDownClass()
        
        if is_ci:
            print ("SESSIONID: " + self.selenium.session_id)
            pass_status = environ["TRAVIS_TEST_RESULT"] == '0'
            set_test_status(self.selenium.session_id, passed=pass_status)

        self.selenium.quit()

    def test_admin(self):
        self.selenium.get(self.live_server_url + '/admin')

        self.selenium.find_element(By.ID, 'id_username')

    def test_about(self):
        self.selenium.get(self.live_server_url + '/about')

        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sander Maijers', body.text)

    def test_all_centres(self):
        self.selenium.get(self.live_server_url + '/all_centres')

        table = self.selenium.find_element(By.ID, 'all_centres')
        table.find_element(By.TAG_NAME, 'tr')

    def test_centre(self):
        self.selenium.get(self.live_server_url + '/centre/1')

        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('Karls', body.text)

    def test_contact_in_centre(self):
        self.selenium.get(self.live_server_url + '/centre/1')
        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('Margarethe Weber', body.text)

    def test_centres_contacts(self):
        self.selenium.get(self.live_server_url + '/centres_contacts')

        table = self.selenium.find_element(By.ID, 'centres_contacts')
        table.find_element(By.TAG_NAME, 'tr')

    def test_consortia(self):
        self.selenium.get(self.live_server_url + '/consortia')

        table = self.selenium.find_element(By.ID, 'consortia')
        table.find_element(By.TAG_NAME, 'tr')

    def test_contacting(self):
        self.selenium.get(self.live_server_url + '/contacting')

        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('Contacting', body.text)

    def test_contact(self):
        self.selenium.get(self.live_server_url + '/contact/1')

        table = self.selenium.find_element(By.ID, 'contact')
        self.assertIn('ePPN', table.text)

    def test_fcs(self):
        self.selenium.get(self.live_server_url + '/fcs')

        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('FCS endpoint', body.text)

    def test_map(self):
        self.selenium.get(self.live_server_url + '/map')

        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('geographical overview', body.text)

    def test_oai_pmh(self):
        self.selenium.get(self.live_server_url + '/oai_pmh')

        table = self.selenium.find_element(By.ID, 'oai-pmh_endpoints')
        table.find_element(By.TAG_NAME, 'tr')

    def test_spf(self):
        self.selenium.get(self.live_server_url + '/spf')

        table = self.selenium.find_element(By.ID, 
            'saml_service_providers_and_identity_federations')
        table.find_element(By.TAG_NAME, 'tr')
