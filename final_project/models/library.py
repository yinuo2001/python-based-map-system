'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the model file for class Library.
'''

THRESHOLD_KILOMETER = 1.2


class Library:
    '''
    Represents a library with attributes of name, longitude, latitude,
    url link and address.
    Attributes:
        name(str): the library's name
        longitude(float): the library's coordinate longitude
        latitude(float): the library's coordinate latitude
        url(str): the library public website's url link
        address(str): the library's address
    '''
    def __init__(self, name, longitude, latitude, url, address):
        '''
        This is the constructor for the class Library.
        Parameters:
            name(str): the station's name
            longitude(float): the station's coordinate longitude
            latitude(float): the station's coordinate latitude
            url(str): the library public website's url link
            address(str): the library's address
        Returns:
            nothing
        Raises:
            TypeError: if longitude or latitude is not a float
                       if name, url or address is not a string
        '''
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(longitude, float) or not isinstance(latitude, float):
            raise TypeError("Longitude and latitude must be floats.")
        if not isinstance(url, str):
            raise TypeError("Url link must be a string.")
        if not isinstance(address, str):
            raise TypeError("Address must be a string.")
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.url = url
        self.address = address

    def __eq__(self, other):
        '''
        This method substitutes for '==' in class Library. It compares if two
        objects of the same type have the same name.
        Parameters:
            nothing
        Returns:
            True if the two objects are of the same type and name,
            otherwise False
        '''
        if isinstance(other, Library):
            if self.name == other.name:
                return True
        return False

    def __str__(self):
        '''
        This method substitutes for print() in class Library.
        It prints name and address of a library.
        Parameters:
            nothing
        Returns:
            A string including name and address of the Library object
        '''
        return self.name

    def find_nearby_stations(self, station_list: list):
        '''
        Finds all nearby stations of the library object.
        Parameters:
            station_list: a list containing all station objects
        Raises:
            TypeError: if station_list is not a list
            AttributeError: if elements in station_list are not all
            station objects
        '''
        # In order to prevent circular import (import Library in Station and
        # import Station in Library), I choose not to use isinstance() to
        # raise the AttributeError but try-except
        try:
            if not isinstance(station_list, list):
                raise TypeError(
                    "A list of stations is needed to find nearby stations.")
            nearby_station_list = list()
            for station in station_list:
                distance = station.calculate_distance_from_library(self)
                if distance <= THRESHOLD_KILOMETER:
                    nearby_station_list.append(station)
            self.nearby_stations = nearby_station_list
        except AttributeError:
            raise AttributeError(
                "The elements in station_list must be Station objects.")
