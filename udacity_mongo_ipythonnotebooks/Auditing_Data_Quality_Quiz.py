#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def strType(var):
    try:
        if int(var) == float(var):
            return 'int'
    except:
        try:
            float(var)
            return 'float'
        except:
            return 'other'

def audit_file(filename, fields):
    fieldtypes = {}
    

    # YOUR CODE HERE
    
    dfields= {key: [] for key in FIELDS} 
    
    
    
    with open('cities.csv', "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        
        for line in reader:
            if 'dbpedia.org' in line['URI']:
                for field in FIELDS:
                    val = line[field]
                    if strType(val) == 'int':
                        dfields[field].append(type(1))
                        fieldtypes[field] = set(dfields[field])
                    elif strType(val) == 'float':
                        dfields[field].append(type(1.1))
                        fieldtypes[field] = set(dfields[field])
                    elif val == 'NULL' or line[field] == "":
                        dfields[field].append(type(None))
                        fieldtypes[field] = set(dfields[field])
                    elif val.startswith('{'):
                        dfields[field].append(type([]))
                        fieldtypes[field] = set(dfields[field])
                    else:
                        dfields[field].append(type('str'))
                        fieldtypes[field] = set(dfields[field])

        return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
