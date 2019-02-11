#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 Assignment - Diandra Vega"""


import urllib2
import csv
import datetime
import logging
import argparse
import os


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--url", help="Add a URL to use in script.")
ARGS = PARSER.parse_args()


if ARGS.url:
    USER_INPUT = raw_input('Enter an ID number to search for: ')
else:
    print "No URL specified. Please see 'python assignment2_part1.py' -h" +\
          " for help."
    os.system('python assignment2_part1.py -h')
    print "Exiting . . ."
    exit()


def downloadData(filename):
    """Download CSV file from URL inputted in --url parameter.

    ARGS:
        filename (str): Input URL of file to download here.

    RETURNS:
        object: Return is the contents inside CSV file download as an object.

    EXAMPLES:
        >>> downloadData('
        https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
    """
    response = urllib2.urlopen(filename)
    return response


def processData(readfile):
    """This will process the data downloaded from the URL in downloadData().
    CSV Data will be turned into a dict, with ID numbers becoming the keys
    and birthdays plus names becoming key values.

    ARGS:
        readfile (obj): Argument should be object downloaded with
            downloadData().

    RETURNS:
        dict: Returns a dictionary processed from CSV object content.

    EXAMPLES:
        >>> processData(downloadData('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'))

        >>> data = downloadData('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
        >>> processData(data)
    """
    datafile = csv.DictReader(readfile)
    birthday_data = {}
    counter = 0

    for row in datafile:
        """Iterate over CSV"""
        for key, val in row.iteritems():
            """By default, each key comes out with column header names. Flip
            the 'id' column to make the value the new key instead with empty
            values."""
            if key == "id":
                id_num = val
                birthday_data[id_num] = None
        for key, val in row.iteritems():
            """Once new keys are in place, start pulling data for tuples."""
            if key == "name":
                name = val
        for key, val in row.iteritems():
            """Process the birthday column and pull data to be added to
            tuples."""
            counter += 1
            if key == "birthday":
                format = "%d/%m/%Y"
                try:
                    temp_bd = datetime.datetime.strptime(val, format).date()
                except ValueError:
                    logging.basicConfig(filename='errors.log',
                                        level=logging.ERROR)
                    assignment2 = logging.getLogger('assignment2')
                    assignment2.setLevel(logging.ERROR)
                    assignment2.error('Error processing line #: ' + str(counter) +
                                  ' for ID #: ' + id_num + '.' )
                else:
                    birthday = str(temp_bd)
                    birthday_data[id_num] = (name, birthday)

    for key, val in birthday_data.items():
        """Clean up the new dictionary by removing keys with 'None' values due
        to date processing errors."""
        if val == None:
            birthday_data.pop(key, None)
    return birthday_data


def displayPerson(id, personData):
    """Print processed output from processData() in user-friendly format.

    ARGS:
        id (int): Will be an integer value of an ID # you want to lookup. This
            will call the key from a dictionary.
        personData (dict): Will be a dictionary produced from processData()
            function.

    RETURNS:
        str: Returns a formatted string with data pulled from dict values.

    EXAMPLES:
        >>> csvData = downloadData('
        https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
        >>> displayPerson(12, processData(csvData))
        >>> Person #:24 is Stewart Bond with a birthday of 2008-02-15.
    """
    try:
        name = personData[str(id)][0]
        birthday = personData[str(id)][1]
        result = "Person #:{0} is {1} with a birthday of {2}.".format(
            id, name, birthday)
    except KeyError:
        result = "No user is found with that id."
    return result


def main(url):
    """Main function that will download CSV data then process it. If an error
    is encountered, the program will exit.

    ARGS:
        url (str): This will be the URL you are downloading CSV data from.

    RETURNS:
        dict: Returns processed dictionary produced from CSV file data.

    EXAMPLES:
        >>> main('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
    """
    try:
        csvData = downloadData(url)
        personData = processData(csvData)
    except Exception as error_type:
        raise (error_type)
        exit()
    return personData


RESULT = main(ARGS.url)


if int(USER_INPUT) <= 0:
    """Check if user input is a valid key value. When not valid, 
    exit program."""
    print "Invalid number. Exiting . . ."
    exit()
else:
    while int(USER_INPUT) > 0:
        """If key value is valid, continue asking user for different values."""
        print displayPerson(USER_INPUT, RESULT)
        USER_INPUT = raw_input('Enter an ID number to search for: ')
        if int(USER_INPUT) <= 0:
            print "Invalid number. Exiting . . ."
            break