'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This test file uses unittest module to test read_data function.
'''
import unittest
import requests_mock
import requests
from requests.exceptions import HTTPError, TooManyRedirects


class TestReadData(unittest.TestCase):
    def test_read_data(self):
        test_url = "https://opendata.vancouver.ca/api/explore/v2.1/" + \
                   "catalog/datasets/libraries/records?limit=100&offset=0&" + \
                   "timezone=UTC&include_links=false&include_app_metas=false"
        expected_data = {"results": {
            "address": "7110 Kerr St",
            "name": "Champlain Heights",
            "urllink":
            "http://www.vpl.ca/branches/details/champlain_heights_branch",
            "geom": {"type": "Feature",
                     "geometry":
                     {"coordinates": [-123.0402, 49.2191],
                      "type": "Point"},
                     "properties": {}},
            "geo_local_area": "Killarney",
            "geo_point_2d": {"lon": -123.0402, "lat": 49.2191}}}
        with requests_mock.Mocker() as m:
            m.get(test_url, json=expected_data)
            response = requests.get(test_url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["results"]["name"],
                             "Champlain Heights")

    def test_read_data_url_wrong_type(self):
        test_wrong_type_url = 123123123
        with requests_mock.Mocker() as m:
            m.get(test_wrong_type_url)
            self.assertRaises(TypeError)

    def test_read_data_with_http_error(self):
        test_wrong_url = "https://thisisawrongurl"
        with requests_mock.Mocker() as m:
            m.get(test_wrong_url, status_code=404)
            self.assertRaises(HTTPError)

    def test_read_data_with_connection_error(self):
        test_url = "https://opendata.vancouver.ca/api/explore/v2.1/" + \
                   "catalog/datasets/libraries/records?limit=100&offset=0&" + \
                   "timezone=UTC&include_links=false&include_app_metas=false"

        with requests_mock.Mocker() as m:
            m.get(test_url, exc=ConnectionError)
            self.assertRaises(ConnectionError)

    def test_read_data_with_toomanyredirects(self):
        test_url = "https://opendata.vancouver.ca/api/explore/v2.1/" + \
                   "catalog/datasets/libraries/records?limit=100&offset=0&" + \
                   "timezone=UTC&include_links=false&include_app_metas=false"
        with requests_mock.Mocker() as m:
            m.get(test_url, exc=TooManyRedirects)
            self.assertRaises(TooManyRedirects)

    def test_read_data_with_timeouterror(self):
        test_url = "https://opendata.vancouver.ca/api/explore/v2.1/" + \
                   "catalog/datasets/libraries/records?limit=100&offset=0&" + \
                   "timezone=UTC&include_links=false&include_app_metas=false"
        with requests_mock.Mocker() as m:
            m.get(test_url, exc=TimeoutError)
            self.assertRaises(TimeoutError)
