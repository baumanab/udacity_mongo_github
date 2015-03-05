# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
        
        tagsd = {}
        
        for event, elem in ET.iterparse(filename):
            if event == 'end':
                
                if elem.tag not in tagsd.keys():
                    tagsd[elem.tag] = 1
                else:
                    tagsd[elem.tag] +=1
            elem.clear()
        return tagsd


