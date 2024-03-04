'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the function file for creating objects using the data fetched.
'''

from models.station import Station
from models.library import Library


def create_list_of_station_objects(data: dict) -> list:
    '''
    Create Station objects from the data
    Parameters:
        data (dict): a dictionary extracted from the API
    Returns:
        a list including all station objects
    Raises:
        TypeError: if the parameter is not a dictionary
        KeyError: if the data does not have certain keys
    '''
    try:
        if not isinstance(data, dict):
            raise TypeError("The data must be a dictionary.")
        station_list = list()
        for station_information in data["results"]:
            longitude = round(float(
                station_information["geom"]["geometry"]["coordinates"][0]), 4)
            latitude = round(float(
                station_information["geom"]["geometry"]["coordinates"][1]), 4)
            station = Station(
                station_information["station"], longitude, latitude)

            # There are two stations with the same name (Waterfront)
            # very close to each other. In order to prevent confusion,
            # I decided to keep one Waterfront only.
            if station not in station_list:
                station_list.append(station)
        return station_list

    except KeyError:
        raise KeyError("The key does not exist.")


def create_list_of_library_objects(data: dict) -> list:
    '''
    Create Library objects from the data
    Parameters:
        data (dict): a dictionary extracted from the API
    Returns:
        a list including all library objects
    Raises:
        TypeError: if the parameter is not a dictionary
        KeyError: if the data does not have certain keys
    '''
    try:
        if not isinstance(data, dict):
            raise TypeError("The data must be a dictionary.")
        library_list = list()
        for library_information in data["results"]:
            url = library_information["urllink"]
            name = library_information["name"]
            address = library_information["address"]
            longitude = float(library_information
                              ["geo_point_2d"]["lon"])
            latitude = float(library_information
                             ["geo_point_2d"]["lat"])
            library = Library(name, longitude, latitude, url, address)
            library_list.append(library)
        return library_list

    except KeyError:
        raise KeyError("The key does not exist.")
