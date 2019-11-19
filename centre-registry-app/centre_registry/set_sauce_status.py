#!/usr/bin/env python3

from os import environ
import http.client
import base64
try:
    import json
except ImportError:
    import simplejson as json

config = {"username": environ["SAUCE_USERNAME"],
          "access-key": environ["SAUCE_ACCESS_KEY"]}

pass_status = True if environ["TRAVIS_TEST_RESULT"] == 0 else False

base64string = str(base64.b64encode(bytes('%s:%s' % (config['username'], config['access-key']),'utf-8')))[1:]

def set_test_status(jobid, passed=True):
    body_content = json.dumps({"passed": passed})
    connection =  http.client.HTTPSConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (config['username'], jobid),
                       body_content,
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200

set_test_status(environ["TRAVIS_BUILD_NUMBER"], passed=pass_status)