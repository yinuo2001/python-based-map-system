'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the model file for class Library.
'''


CONVERSION_FACTOR = 111  # converts coordinate to kilometer


class Station:
    '''
    Represents a station with attributes of name, longitude and latitude.
    Attributes:
        name(str): the station's name
        longitude(float): the station's coordinate longitude
        latitude(float): the station's coordinate latitude
    '''
    def __init__(self, name: str, longitude: float, latitude: float):
        '''
        This is the constructor for the class Station.
        Parameters:
            name(str): the station's name
            longitude(float): the station's coordinate longitude
            latitude(float): the station's coordinate latitude
        Returns:
            nothing
        Raises:
            TypeError: if longitude or latitude is not a float
                       if name is not a string
        '''
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(longitude, float) or not isinstance(latitude, float):
            raise TypeError("Longitude and latitude must be floats.")
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        '''
        This method substitutes for '==' in class Station. It compares if two
        objects of the same type have the same name.
        Parameters:
            nothing
        Returns:
            True if the two objects are of the same type and name,
            otherwise False
        '''
        if isinstance(other, Station):
            if self.name == other.name:
                return True
        return False

    def __str__(self):
        '''
        This method substitutes for print() in class Station.
        It prints name and coordinates of a station.
        Parameters:
            nothing
        Returns:
            A string including name and coordinates of the Station object
        '''
        information = f"Station {self.name} is at ({self.longitude},\
{self.latitude})."
        return information

    def calculate_distance_from_library(self, library) -> float:
        '''
        This method calculates the distance between the station
        object and a library object.
        Parameters:
            library: a library object
        Returns a float representing the distance
        Raises:
            AttributeError: if library is not a Library object
        '''
        # In order to handle errors and prevent circular import, and
        # since this method has one possible error, I choose not to
        # use isinstance() to raise the AttributeError but try-except
        try:
            difference_lat_kilometer = (
                library.latitude - self.latitude) * CONVERSION_FACTOR
            difference_lon_kilometer = (
                library.longitude - self.longitude) * CONVERSION_FACTOR
            distance = (difference_lat_kilometer ** 2 +
                        difference_lon_kilometer ** 2) ** (1/2)
            return round(distance, 2)
        except AttributeError:
            raise AttributeError(
                "Given parameter must belong to class Library.")
