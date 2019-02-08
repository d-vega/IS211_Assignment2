#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 2 Assignment, Part 1"""


import urllib2
import csv
import datetime
import logging


URL = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
LOG_FILENAME = "assignment2_output.log"
LEVELS = { 'debug': logging.DEBUG,
           'info': logging.INFO,
           'warning': logging.ERROR,
           'error': logging.ERROR,
           'critical': logging.CRITICAL
           }


#### May not need this class. TBD ####
class ConvertDateException(Exception):
    """Convert date exception class"""
    logging.basicConfig(level=logging.ERROR)


def downloadData(filename):
    """Pretty docstring here"""
    response = urllib2.urlopen(filename)
    # result = response.read()
    return response


def processData(readfile=downloadData(URL)):
    """2nd pretty docstring"""
    datafile = csv.DictReader(readfile)
    birthday_data = {}
    counter = 0

    for row in datafile:
        for key, val in row.iteritems():
            if key == "id":
                id_num = val
                birthday_data[id_num] = None
        for key, val in row.iteritems():
            if key == "name":
                name = val
        for key, val in row.iteritems():
            counter += 1
            if key == "birthday":
                dateformat = "%d/%m/%Y"
                try:
                    temp_bd = datetime.datetime.strptime(val, dateformat).date()
                except ValueError:
                    logging.error('Error processing line #: ' + str(counter) + ' for ID #: ' + id_num + '.' )
                else:
                    #birthday = temp_bd.strftime(dateformat)
                    birthday = str(temp_bd)
                    birthday_data[id_num] = (name, birthday)
    return birthday_data


print processData()
