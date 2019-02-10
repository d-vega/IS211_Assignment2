#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 Assignment, Part 1"""


import urllib2
import csv
import datetime
import logging
import argparse
import os


USER_INPUT = raw_input('Enter an ID number to search for: ')
PARSER = argparse.ArgumentParser()
PARSER.add_argument("--url", help="Add a URL to use in script.")
ARGS = PARSER.parse_args()


if ARGS.url:
    pass
else:
    print "No URL specified. Please see 'python assignment2_part1.py -h for" +\
          " help."
    os.system('python assignment2_part1.py -h')
    print "Exiting . . ."
    exit()


def downloadData(filename):
    """Pretty docstring here"""
    response = urllib2.urlopen(filename)
    # result = response.read()
    return response


def processData(readfile):
    """2nd pretty docstring"""
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
    """3rd pretty docstring"""
    try:
        name = personData[str(id)][0]
        birthday = personData[str(id)][1]
        result = "Person #:{0} is {1} with a birthday of {2}.".format(
            id, name, birthday)
    except KeyError:
        result = "No user is found with that id."
    return result


def main(url):
    """Main function"""
    try:
        csvData = downloadData(url)
        personData = processData(csvData)
    except Exception as error_type:
        raise (error_type)
        exit()
    return personData


RESULT = main(ARGS.url)


if int(USER_INPUT) <= 0:
    print "Invalid number. Exiting . . ."
    exit()
else:
    while int(USER_INPUT) > 0:
        print displayPerson(USER_INPUT, RESULT)
        USER_INPUT = raw_input('Enter an ID number to search for: ')
        if int(USER_INPUT) <= 0:
            print "Invalid number. Exiting . . ."
            break