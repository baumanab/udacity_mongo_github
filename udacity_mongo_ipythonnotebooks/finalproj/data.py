# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import time
from audit import *

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_ref": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    # This function of code feeds into the iterparse initialized in process_map.
    address = {}
    node = {}
    # this section extracts the first level tag string from the cursor element
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        created = {}
        pos = []
        noderef = []
        node['type'] = element.tag
        
        # This subsection iterates over the items contained between the start and end 'node' and 'way' tags
        # creating key:value pairs, and appending them to the node dict.
        for cursor in element.iter(element.tag):
            for label in cursor.attrib:
                val = cursor.attrib[label]
                if label in CREATED:
                    created[label] = val
                    
                if label == 'lat' or label == 'lon':
                    pos.append(float(val)) 
                    
                else:
                    if label not in CREATED:
                        node[label] = val
            node['created'] = created
            node['pos'] = sorted(pos,reverse=True)
            
        # This section of code iterates over the second level nd tag, where nd below is a cursor, then places
        # the nd values in an array, updates the value of the noderef dict to this array, then appends
        #it to the node dict.
        for nd in element.iter('nd'):        
            noderef.append(nd.attrib['ref'])
            
            node['node_refs'] = noderef
        
        # This section of code iterates over the second level 'k' and 'v' tags, checks for problem
        # characters, and assembles the node dict with specific boolean criteria. Note that to assemble
        # the address dict properly it has to be initialized above this code block, otherwise you
        # reset it with every tag iteration.
        for tag in element.iter('tag'):
            
            tagk = tag.attrib['k']
            tagv = tag.attrib['v']
            m = problemchars.search(tagk)
            if not m:
                if tagk == "addr:street":
				    address['street'] = update_name(tagv,mapping)             
             
                elif tagk == 'addr:housenumber':                 
                    address['housenumber'] = tagv                    
                    node['address'] = address                      
                   
                elif 'addr' not in tagk:
                    node[tagk] = tagv
                else:
                    pass  
        
        return node
    # if element.tag != to 'node' or 'way', bypass the other loops, and return none.
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    context = iter(ET.iterparse(file_in, events=('start', 'end')))
    _, root = context.next()
 
    with codecs.open(file_out, "w") as fo:  
        for event, element in context:
        	if event == 'end':
	            el = shape_element(element)                        
	            if el:
	                if pretty:
	                    fo.write(json.dumps(el, indent=2)+"\n")
	                else:
	                    fo.write(json.dumps(el) + "\n")
	            root.clear()
            
                

                    
            
        
    

