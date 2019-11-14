from os import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


# TODO: remove
# try:
# except ImportError:
# from selenium.webdriver.chrome.webdriver import WebDriver


class SystemTestCase(StaticLiveServerTestCase):
    fixtures = ['test_data.json']

    @classmethod
    def setUpClass(cls):
        # TODO: Replace Travis CI & Sauce Labs with generic testing code.
        is_ci = (environ.get('TRAVIS') or '').lower() == 'true'
        if is_ci:
            from selenium.webdriver import Remote
            hub_url = ("{username:s}:{access_key:s}@ondemand.eu-central-1.saucelabs.com"
                .format(
                username=environ["SAUCE_USERNAME"],
                access_key=environ["SAUCE_ACCESS_KEY"]))
            desired_capabilities = {
                "browserName": environ["browserName"],
                "build": environ["TRAVIS_BUILD_NUMBER"],
                "platform": environ["platform"],
                "tags": [environ["TRAVIS_PYTHON_VERSION"], "CI"],
                "tunnel-identifier": environ["myTunnel01"],
                "version": environ["version"]
            }
            cls.selenium = Remote(
                desired_capabilities=desired_capabilities,
                command_executor="https://{hub_url:s}/wd/hub"
                    .format(hub_url=hub_url))
        else:
            cls.selenium = WebDriver()
        super(SystemTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SystemTestCase, cls).tearDownClass()
        cls.selenium.quit()

    def test_admin(self):
        self.selenium.get(self.live_server_url + '/admin')

        self.selenium.find_element_by_id('id_username')

    def test_about(self):
        self.selenium.get(self.live_server_url + '/about')

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Sander Maijers', body.text)

    def test_all_centres(self):
        self.selenium.get(self.live_server_url + '/all_centres')

        table = self.selenium.find_element_by_id('all_centres')
        table.find_element_by_tag_name('tr')

    def test_centre(self):
        self.selenium.get(self.live_server_url + '/centre/1')

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Karls', body.text)

    def test_centres_contacts(self):
        self.selenium.get(self.live_server_url + '/centres_contacts')

        table = self.selenium.find_element_by_id('centres_contacts')
        table.find_element_by_tag_name('tr')

    def test_consortia(self):
        self.selenium.get(self.live_server_url + '/consortia')

        table = self.selenium.find_element_by_id('consortia')
        table.find_element_by_tag_name('tr')

    def test_contacting(self):
        self.selenium.get(self.live_server_url + '/contacting')

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Contacting', body.text)

    def test_contact(self):
        self.selenium.get(self.live_server_url + '/contact/1')

        table = self.selenium.find_element_by_id('contact')
        self.assertIn('ePPN', table.text)

    def test_fcs(self):
        self.selenium.get(self.live_server_url + '/fcs')

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('FCS endpoint', body.text)

    def test_map(self):
        self.selenium.get(self.live_server_url + '/map')

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('geographical overview', body.text)

    def test_oai_pmh(self):
        self.selenium.get(self.live_server_url + '/oai_pmh')

        table = self.selenium.find_element_by_id('oai-pmh_endpoints')
        table.find_element_by_tag_name('tr')

    def test_spf(self):
        self.selenium.get(self.live_server_url + '/spf')

        table = self.selenium.find_element_by_id(
            'saml_service_providers_and_identity_federations')
        table.find_element_by_tag_name('tr')
