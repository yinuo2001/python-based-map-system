'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This test file uses unittest module to test class Library.
'''

import unittest
from models.library import Library
from models.station import Station  # To test method find_nearby_stations


class LibraryTest(unittest.TestCase):
    '''
    Unittests for the Library class.
    '''
    def test_library_init(self):
        library = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        self.assertIsInstance(library, Library)
        self.assertEqual(library.name, "Firehall")
        self.assertEqual(library.longitude, -123.1376)
        self.assertEqual(library.latitude, 49.2629)
        self.assertEqual(
            library.url,
            "http://www.vpl.ca/branches/details/firehall_branch")
        self.assertEqual(library.address, "1455 W 10th Av")

    def test_library_init_name_wrong_type(self):
        with self.assertRaises(TypeError):
            Library(1, -123.1376, 49.2629,
                    "http://www.vpl.ca/branches/details/firehall_branch",
                    "1455 W 10th Av")

    def test_library_init_longitude_wrong_type(self):
        with self.assertRaises(TypeError):
            Library("Firehall", "-123.1376", 49.2629,
                    "http://www.vpl.ca/branches/details/firehall_branch",
                    "1455 W 10th Av")

    def test_library_init_latitude_wrong_type(self):
        with self.assertRaises(TypeError):
            Library("Firehall", -123.1376, "49.2629",
                    "http://www.vpl.ca/branches/details/firehall_branch",
                    "1455 W 10th Av")

    def test_library_init_url_wrong_type(self):
        with self.assertRaises(TypeError):
            Library("Firehall", -123.1376, 49.2629,
                    12345, "1455 W 10th Av")

    def test_library_init_address_wrong_type(self):
        with self.assertRaises(TypeError):
            Library("Firehall", "-123.1376", 49.2629,
                    "http://www.vpl.ca/branches/details/firehall_branch",
                    145510)

    def test_library_eq_same_name(self):
        library_1 = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        library_2 = Library(
            "Firehall", 49.2629, -123.1376,
            "this is a completely different url",
            "this is a completely different address")
        self.assertTrue(library_1 == library_2)

    def test_library_eq_different_name_same_other_information(self):
        library_1 = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        library_2 = Library(
            "this is a completely different name", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        self.assertFalse(library_1 == library_2)

    def test_library_eq_not_even_a_library(self):
        library_1 = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        library_2 = ("Firehall", 49.2629, -123.1376,
                     "this is a completely different url",
                     "this is a completely different address")
        self.assertFalse(library_1 == library_2)

    def test_library_str(self):
        library = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        self.assertEqual(str(library), "Firehall")

    def test_library_find_nearby_stations_no_nearby_stations(self):
        library_with_no_nearby_stations = Library(
            "Firehall", -123.1376, 49.2629,
            "http://www.vpl.ca/branches/details/firehall_branch",
            "1455 W 10th Av")
        a_station = Station("Main Street - Science World",
                            -123.1006, 49.2732)
        self.assertEqual(
            library_with_no_nearby_stations.find_nearby_stations([a_station]),
            [])

    def test_library_find_nearby_stations_have_nearby_stations(self):
        library_with_nearby_stations = Library(
            "Mount Pleasant", -123.1002, 49.2643,
            "http://www.vpl.ca/branches/details/mount_pleasant_branch",
            "1 Kingsway")
        a_station = Station("Main Street - Science World",
                            -123.1006, 49.2732)
        self.assertEqual(
            library_with_nearby_stations.find_nearby_stations([a_station]),
            [a_station])

    def test_library_find_nearby_stations_parameter_not_a_list(self):
        library = Library(
            "Mount Pleasant", -123.1002, 49.2643,
            "http://www.vpl.ca/branches/details/mount_pleasant_branch",
            "1 Kingsway")
        a_station = Station("Main Street - Science World",
                            -123.1006, 49.2732)
        station_tuple = (a_station)
        with self.assertRaises(TypeError):
            library.find_nearby_stations(station_tuple)

    def test_library_find_nearby_stations_not_station_objects(self):
        library = Library(
            "Mount Pleasant", -123.1002, 49.2643,
            "http://www.vpl.ca/branches/details/mount_pleasant_branch",
            "1 Kingsway")
        coordinates = [-123.1006, 49.2732]
        with self.assertRaises(AttributeError):
            library.find_nearby_stations(coordinates)
