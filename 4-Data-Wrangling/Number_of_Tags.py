import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

'''
The code below is to find out how many types of tags are there and the number of each tag.
'''

def count_tags(filename):
    tags = {}
    for event, element in ET.iterparse(filename):
        if element.tag not in tags.keys():
            tags[element.tag] = 1
        else:
            tags[element.tag] += 1
    return tags

def test():

    tags = count_tags('san-jose_california.osm')
    pprint.pprint(tags)

if __name__ == "__main__":
    test()