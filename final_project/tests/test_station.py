'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This test file uses unittest module to test class Station.
'''

import unittest
from models.station import Station
from models.library import Library  # To test the distance calculation method


class StationTest(unittest.TestCase):
    '''
    Unittests for the Station class.
    '''
    def test_station_init(self):
        station = Station("Rupert", -123.0328, 49.2607)
        self.assertIsInstance(station, Station)
        self.assertEqual(station.name, "Rupert")
        self.assertEqual(station.longitude, -123.0328)
        self.assertEqual(station.latitude, 49.2607)

    def test_station_init_name_wrong_type(self):
        with self.assertRaises(TypeError):
            Station(1, -123.0328, 49.2607)

    def test_station_init_longitude_wrong_type(self):
        with self.assertRaises(TypeError):
            Station("Rupert", "-123.03282", 49.2607)

    def test_station_init_latitude_wrong_type(self):
        with self.assertRaises(TypeError):
            Station("Rupert", -123.0328, "49.2607")

    def test_station_eq_same_name_different_coordinates(self):
        station_1 = Station("Rupert", -123.0328, 49.2607)
        station_2 = Station("Rupert", 49.2607, -123.0328)
        self.assertTrue(station_1 == station_2)

    def test_station_eq_different_name_same_coordinates(self):
        station_1 = Station("Rupert", -123.0328, 49.2607)
        station_2 = Station("Waterfront", -123.0328, 49.2607)
        self.assertFalse(station_1 == station_2)

    def test_station_eq_not_a_station(self):
        station_1 = Station("Rupert", -123.0328, 49.2607)
        station_2 = ("Waterfront", -123.0328, 49.2607)
        self.assertFalse(station_1 == station_2)

    def test_station_str(self):
        station = Station("Rupert", -123.0328, 49.2607)
        self.assertEqual(str(station),
                         "Station Rupert is at (-123.0328,49.2607).")

    def test_station_calculate_distance_from_library(self):
        station = Station("29th Avenue", -123.0459, 49.2442)
        library = Library("Renfrew", -123.043, 49.2524,
                          "http://www.vpl.ca/branches/details/renfrew_branch",
                          "2969 E 22nd Av")
        self.assertEqual(station.calculate_distance_from_library(
            library), 0.97)

    def test_station_calculate_distance_from_library_not_library_object(self):
        station = Station("29th Avenue", -123.0459, 49.2442)
        coordinates = (-123.043, 49.2524)
        with self.assertRaises(AttributeError):
            station.calculate_distance_from_library(coordinates)
