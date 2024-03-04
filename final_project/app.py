'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the driver file.
'''

import streamlit as st
from util import read_data, process_data
import view.input_widgets as inp
import view.output_visualization as out
from requests.exceptions import TooManyRedirects, HTTPError


STATION_URL = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/" + \
              "datasets/rapid-transit-stations/records?limit=100&offset=0" + \
              "&timezone=UTC&include_links=false&include_app_metas=false"
LIBRARY_URL = "https://opendata.vancouver.ca/api/explore/v2.1/" + \
              "catalog/datasets/libraries/records?limit=100&offset=0&" + \
              "timezone=UTC&include_links=false&include_app_metas=false"


def map_render(library_data: dict, station_data: dict):
    '''
    The first page of view, creates two kinds of maps based on user's choice
    in the selectbox.
    Parameters:
        library_data: a dictionary of library data
        station_data: a dictionary of station data
    Raises:
        TypeError: if library data or station data is not a dictionary
    '''
    if not isinstance(library_data, dict):
        raise TypeError("Library data must be a dictionary.")
    if not isinstance(station_data, dict):
        raise TypeError("Station data must be a dictionary.")
    # This map page will basically show two kinds of map
    st.subheader("Library-Station Map")
    if "library" not in st.session_state:
        library_list = process_data.create_list_of_library_objects(
             library_data)
        st.session_state["library"] = library_list
    library_option = inp.display_selectbox("Where do you want to go?",
                                           st.session_state["library"])
    # By default, the map including all libraries and stations is displayed,
    # because by default library_option is None
    if library_option is None:
        if "station" not in st.session_state:
            station_list = process_data.create_list_of_station_objects(
                station_data)
            st.session_state["station"] = station_list
        out.display_map_with_all_libraries(st.session_state["station"],
                                           st.session_state["library"])
    # If the user selects from the selectbox, the first type of map
    # including only one library and its nearby stations is displayed
    else:
        # If the user made their choice, more information about this
        # specific library is given
        add_button = inp.display_button("Add into want-to-go list")
        # The user uses the add button to add any libraries
        # into their fav list
        if add_button is True:
            if library_option not in st.session_state["favourite list"]:
                st.success("Successfully added!")
                st.session_state["favourite list"].append(library_option)
            else:
                st.warning("You already have this library!")
        # Find nearby stations of the chosen library

        library_option.find_nearby_stations(st.session_state["station"])

        if library_option.nearby_stations == []:
            st.write("This library has no nearby stations. \
                     Select another libray if you wish!")
        else:
            st.caption("Nearby stations are:")
            distance_list = list()
            nearby_station_name_list = list()
            # Calculate distance between nearby stations and the library
            for station in library_option.nearby_stations:
                distance = station.calculate_distance_from_library(
                    library_option)
                distance_list.append(distance)
                nearby_station_name_list.append(station.name)
            out.display_dataframe({
                "Station": nearby_station_name_list,
                "Distance(km)": distance_list}, "Distance(km)")

        out.display_map_with_one_library(library_option,
                                         library_option.nearby_stations)


def display_table_render(library_data: dict, station_data: dict):
    '''
    The second page of view, displayed two tables of data
    Parameters:
        library_data: a dictionary of library data
        station_data: a dictionary of station data
    Raises:
        TypeError: if library data or station data is not dictionary
    '''
    if not isinstance(library_data, dict):
        raise TypeError("Library data must be a dictionary.")
    if not isinstance(station_data, dict):
        raise TypeError("Station data must be an dictionary.")
    st.subheader("Tables of Libraries & Stations")
    page_names = ["Libraries", "Stations"]
    page = inp.display_radio("Select the data you want to see!", page_names)

    if page == "Libraries":
        library_name_list = list()
        library_url_list = list()
        library_address_list = list()
        if "library" not in st.session_state:
            library_list = process_data.create_list_of_library_objects(
                library_data)
            st.session_state["library"] = library_list
        for library in st.session_state["library"]:
            library_name_list.append(library.name)
            library_address_list.append(library.address)
            library_url_list.append(library.url)
        library_dictionary = {"Library": library_name_list,
                              "Address": library_address_list,
                              "URL": library_url_list}
        out.display_dataframe(library_dictionary)

    elif page == "Stations":
        station_name_list = list()
        station_longitude_list = list()
        station_latitude_list = list()
        if "station" not in st.session_state:
            station_list = process_data.create_list_of_station_objects(
                station_data)
            st.session_state["station"] = station_list
        for station in st.session_state["station"]:
            station_name_list.append(station.name)
            station_longitude_list.append(station.longitude)
            station_latitude_list.append(station.latitude)
        station_dictionary = {"Station": station_name_list,
                              "Longitude": station_longitude_list,
                              "Latitude": station_latitude_list}
        out.display_dataframe(station_dictionary)


def fav_list_render(favourite_list: list):
    '''
    Displays the favourite list stored in the session state.
    Parameters:
        favourite_list: a list of favourite libraries
    Raises:
        TypeError: if favourite_list is not a list
    '''
    if not isinstance(favourite_list, list):
        raise TypeError("Favourite list must be a list.")
    st.subheader("My Want-to-go List :footprints:")

    if len(favourite_list) >= 1:
        out.display_dataframe({"Favourite libraries": favourite_list})
    else:
        st.write("You currently don't have any favourite libraries. \
                 Add some more in the Maps page!")


def main():
    '''
    This main function controls the workflow of the application.
    '''
    try:
        st.sidebar.title("Navigation")
        # I choose to fetch data when the application starts because
        # most of my features require the same data. Also, the API I
        # chose has limitation of fetching times per minute. But the
        # object creation is done only when invoked by user input.
        library_data = read_data.read_data(LIBRARY_URL)
        station_data = read_data.read_data(STATION_URL)

        if st.sidebar.button("Data Display"):
            st.session_state["page"] = "display"
        if st.sidebar.button("Maps"):
            st.session_state["page"] = "map"
        if st.sidebar.button("Favourite List"):
            st.session_state["page"] = "list"

        if "favourite list" not in st.session_state:
            st.session_state["favourite list"] = []

        if "page" in st.session_state:
            if st.session_state["page"] == "map":
                map_render(library_data, station_data)
            elif st.session_state["page"] == "display":
                display_table_render(library_data, station_data)
            elif st.session_state["page"] == "list":
                fav_list_render(st.session_state["favourite list"])

        st.sidebar.subheader("Instructions:")
        st.sidebar.write("1. Switch between different pages in the sidebar.")
        st.sidebar.write("2. You can see all library and station \
                        information in the first page.")
        st.sidebar.write("3. You can see different maps in the second page.")
        st.sidebar.write("4. Adding libraries in the map page, you can build \
                         your own fav list and see that in the third page!")

    except TypeError as ex:
        print("Type error", type(ex), ex)
    except AttributeError as ex:
        print("Attribute error", type(ex), ex)
    except IndexError as ex:
        print("Index error", type(ex), ex)
    except KeyError as ex:
        print("Key error", type(ex), ex)
    except HTTPError as ex:
        print("HTTP error", type(ex), ex)
    except TooManyRedirects as ex:
        print("Too many redirects", type(ex), ex)
    except ConnectionError as ex:
        print("Connection error", type(ex), ex)
    except TimeoutError as ex:
        print("Time out error", type(ex), ex)


if __name__ == "__main__":
    main()
