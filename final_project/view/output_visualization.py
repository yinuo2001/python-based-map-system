'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the file for output visualization features in View.
'''


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from models.library import Library
from models.station import Station


def display_dataframe(data_dictionary: dict, sorting_item=None):
    '''
    Creates a dataframe using pandas and streamlit dataframe function.
    Parameters:
        data_dictionary: a dictionary of the information displayed in the table
        sorting_item: by default it is None, meaning that the table is
        unsorted. If one of the keys from the data dictionary is provided,
        the table will sort each line accordingly
    Raises:
        TypeError: if data_dictionary is not a dictionary, or
        the provided sorting item is not a string
        KeyError: if the provided sorting item is not a key in
        data_dictionary
    '''
    if not isinstance(data_dictionary, dict):
        raise TypeError("The data must be in the form of a dictionary.")
    if sorting_item is not None:
        if not isinstance(sorting_item, str):
            raise TypeError("The criteria must be in the form of string.")
        if sorting_item not in data_dictionary:
            raise KeyError(
                f"{sorting_item} is not a key in the data dictionary.")

    df = pd.DataFrame(data_dictionary)
    if sorting_item is not None:
        df = df.sort_values(by=sorting_item, ascending=True)
    st.dataframe(df, hide_index=True)


def display_map_with_all_libraries(station_list, library_list):
    '''
    Create a map including all libraries and stations
    Parameters:
        station_list (list): a list of all station objects
        library_list (list): a list of all library objects
    Raises:
        TypeError: if the two parameters are not lists
        IndexError: if the list is empty
        AttributeError: if the list does not have station or library objects
    '''
    if not isinstance(station_list, list):
        raise TypeError("Station_list must be a list.")
    if not isinstance(library_list, list):
        raise TypeError("Library_list must be a list.")
    if library_list == []:
        raise IndexError("Library list must not be empty.")
    for station in station_list:
        if not isinstance(station, Station):
            raise AttributeError(
                "Station list must only contain station objects.")
    for library in library_list:
        if not isinstance(library, Library):
            raise AttributeError(
                "Library list must only contain library objects.")

    default_library = library_list[0]
    default_center = (default_library.latitude, default_library.longitude)

    map = folium.Map(location=default_center, zoom_start=12)

    for library in library_list:
        location = (library.latitude, library.longitude)
        folium.Marker(location,
                      icon=folium.Icon(color="red", icon="book", prefix='fa'),
                      popup=f"<a href='{library.url}' target='_blank'>"
                            f"Library {library.name}</a>").add_to(map)
    for station in station_list:
        location = (station.latitude, station.longitude)
        folium.Marker(location, icon=folium.Icon(
            icon="train", prefix='fa'),
                        popup=f"Station {station.name}").add_to(map)
    st_folium(map)


def display_map_with_one_library(chosen_library, nearby_station_list):
    '''
    Create a map with only one library and its nearby stations.
    Parameters:
        name_library (str): name of the target library
        library_list (list): a list of all library objects
        nearby_station_list (list): a list of station objects near the library
    Raises:
        TypeError: if nearby_station_list is not a list
        AttributeError: if chosen library is not a Library object,
        or elements in nearby_station_list are not Station objects
    '''
    if not isinstance(nearby_station_list, list):
        raise TypeError("Nearby_station_list must be a list.")
    if not isinstance(chosen_library, Library):
        raise AttributeError("Chosen library must be a library object.")
    for station in nearby_station_list:
        if not isinstance(station, Station):
            raise AttributeError(
                "Elements in nearby station list must all be Station objects.")

    map_center = (chosen_library.latitude, chosen_library.longitude)

    map = folium.Map(location=map_center, zoom_start=13)
    folium.Marker(map_center, icon=folium.Icon(color="red", icon="book",
                                               prefix='fa'),
                  popup=f"<a href='{chosen_library.url}' target='_blank'>"
                        f"Library {chosen_library.name}</a>").add_to(map)

    for station in nearby_station_list:
        location = (station.latitude, station.longitude)
        folium.Marker(location, icon=folium.Icon(icon="train", prefix='fa'),
                      popup=f"Station {station.name}").add_to(map)
    st_folium(map)
