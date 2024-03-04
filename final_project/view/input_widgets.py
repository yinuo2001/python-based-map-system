'''
Yinuo Feng
CS 5001, Fall 2023
Final Project
This is the file for input widgets in View.
'''

import streamlit as st


def display_selectbox(title: str, options: list):
    '''
    Displays the streamlit selectbox.
    Parameters:
        title(str): the title of the selectbox
        options(list): a list of options users can choose from
    Returns a selectbox
    Raises:
        TypeError: if the title is not a string, or if the
        options is not a list
    '''
    if not isinstance(title, str):
        raise TypeError("The title must be a string.")
    if not isinstance(options, list):
        raise TypeError("The options must be a list.")
    selectbox = st.selectbox(title, options,
                             index=None, placeholder="Select a library")
    return selectbox


def display_radio(title: str, options: list):
    '''
    Displays the streamlit radio.
    Parameters:
        title(str): the title of the radio
        options(str): a list of options users can choose from
    Returns a radio
    Raises:
        TypeError: if the title is not a string, or if the options
        is not a list
    '''
    if not isinstance(title, str):
        raise TypeError("The title must be a string.")
    if not isinstance(options, list):
        raise TypeError("The options must be a list.")
    radio = st.radio(title, options, index=None)
    return radio


def display_button(label: str):
    '''
    Displays the streamlit button.
    Parameters:
        label(str): the label of the button
    Returns a button
    Raises:
        TypeError: if the label is not a string
    '''
    if not isinstance(label, str):
        raise TypeError("The label must be a string.")
    button = st.button(label)
    return button
