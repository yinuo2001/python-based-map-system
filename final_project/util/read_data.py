'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the function file for fetching data from api.
'''
import requests
from requests.exceptions import HTTPError, TooManyRedirects


def read_data(url: str) -> dict:
    '''
    Fetch data
    Parameters:
        url (str): the url link of the public REST API
    Returns:
        a dictionary of data fetched from the API
    Raises:
        TypeError: if url is not a string
        HTTPError
        TooManyRedirects
        ConnectionError
        TimeoutError
    '''
    try:
        if not isinstance(url, str):
            raise TypeError("The url must be a string.")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except HTTPError:
        raise HTTPError("HTTP error occurs.")
    except TooManyRedirects:
        raise TooManyRedirects("Too many redirects.")
    except ConnectionError:
        raise ConnectionError("Connection error occurs.")
    except TimeoutError:
        raise TimeoutError("Timeout error occurs.")
