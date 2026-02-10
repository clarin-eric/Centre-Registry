from os import environ
import time
import http.client
import base64
import requests

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    import json
except ImportError:
    import simplejson as json


is_ci = environ.get("CI", "").lower() == "true"


def set_test_status(jobid, passed=True):
    base64string = str(
        base64.b64encode(
            bytes('%s:%s' % (environ["SAUCE_USERNAME"], environ["SAUCE_ACCESS_KEY"]), 'utf-8')
        )
    )[1:]
    body_content = json.dumps({"passed": passed})
    connection = http.client.HTTPSConnection("saucelabs.com")
    connection.request(
        'PUT',
        '/rest/v1/%s/jobs/%s' % (environ["SAUCE_USERNAME"], jobid),
        body_content,
        headers={"Authorization": "Basic %s" % base64string}
    )
    result = connection.getresponse()
    return result.status == 200


class SystemTestCase(StaticLiveServerTestCase):
    fixtures = ['test_data.json']
    port = 9999

    @classmethod
    def setUpClass(cls):
        super(SystemTestCase, cls).setUpClass()

        if is_ci:
            hub_url = (
                f"{environ['SAUCE_USERNAME']}:{environ['SAUCE_ACCESS_KEY']}"
                "@ondemand.us-west-1.saucelabs.com"
            )

            match environ["browserName"]:
                case "firefox":
                    options = FirefoxOptions()
                case "chrome":
                    options = ChromeOptions()
                case "MicrosoftEdge":
                    options = EdgeOptions()
                case "internet explorer":
                    options = IeOptions()
                case "safari":
                    options = SafariOptions()

            options.browser_version = environ["browserVersion"]
            options.platform_name = environ["platformName"]
            options.headless = True

            python_location = environ.get("pythonLocation", "")
            python_version = python_location.split("/")[-2] if python_location else None

            sauce_options = {
                "name": "centre-registry_" + environ["GITHUB_RUN_ID"],
                "build": environ["GITHUB_RUN_NUMBER"],
                "tags": [python_version, "CI"],
                "tunnelName": (
                    f"github-tunnel-"
                    f"{environ['browserName']}-"
                    f"{environ['platformName']}-"
                    f"{environ['browserVersion']}-"
                    f"{environ['GITHUB_RUN_ID']}"
                ),
            }

            options.set_capability("sauce:options", sauce_options)

            # Create the driver
            for attempt in range(3):
                try:
                    cls.selenium = Remote(
                        command_executor=f"https://{hub_url}/wd/hub",
                        options=options,
                    )
                    break
                except Exception as e:
                    print(f"Session creation failed: {e}, retrying...")
                    time.sleep(5)
            else:
                raise RuntimeError("Failed to create Sauce Labs session after retries")

            # Print session ID for logs
            print(f"SAUCE_SESSION_ID={cls.selenium.session_id}")

            # Write session ID to file for GitHub Actions
            with open("/tmp/sauce_session_id.txt", "w") as f:
                f.write(cls.selenium.session_id)

            # --- WAIT FOR DJANGO SERVER TO BE READY ---
            for _ in range(30):
                try:
                    r = requests.get(f"{cls.live_server_url}/about")
                    if r.status_code == 200:
                        break
                except Exception:
                    pass
                time.sleep(1)
            else:
                raise RuntimeError("Django test server did not become ready in time")

        else:
            cls.selenium = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        if is_ci:
            print("SAUCE_SESSION_ID=" + cls.selenium.session_id)
            set_test_status(cls.selenium.session_id, passed=True)

        cls.selenium.quit()
        super(SystemTestCase, cls).tearDownClass()

    # --- Helper: navigate with small delay ---
    def go(self, path):
        self.selenium.get(self.live_server_url + path)
        time.sleep(0.5)  # Stabilize Sauce Labs DOM timing

    # --- Helper: wait for element ---
    def wait_for(self, by, value, timeout=10):
        return WebDriverWait(self.selenium, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    # --- TESTS ---

    def test_admin(self):
        self.go('/admin')
        self.wait_for(By.ID, 'id_username')

    def test_about(self):
        self.go('/about')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('Sander Maijers', body.text)

    def test_all_centres(self):
        self.go('/all_centres')
        self.wait_for(By.ID, 'all_centres')

    def test_centre(self):
        self.go('/centre/1')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('Karls', body.text)

    def test_contact_in_centre(self):
        self.go('/centre/1')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('Margarethe Weber', body.text)

    def test_centres_contacts(self):
        self.go('/centres_contacts')
        self.wait_for(By.ID, 'centres_contacts')

    def test_consortia(self):
        self.go('/consortia')
        self.wait_for(By.ID, 'consortia')

    def test_contacting(self):
        self.go('/contacting')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('Contacting', body.text)

    def test_contact(self):
        self.go('/contact/1')
        table = self.wait_for(By.ID, 'contact')
        self.assertIn('ePPN', table.text)

    def test_fcs(self):
        self.go('/fcs')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('FCS endpoint', body.text)

    def test_map(self):
        self.go('/map')
        body = self.wait_for(By.TAG_NAME, 'body')
        self.assertIn('geographical overview', body.text)

    def test_oai_pmh(self):
        self.go('/oai_pmh')
        self.wait_for(By.ID, 'oai-pmh_endpoints')

    def test_spf(self):
        self.go('/spf')
        self.wait_for(By.ID, 'saml_service_providers_and_identity_federations')
