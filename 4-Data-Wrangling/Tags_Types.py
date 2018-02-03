import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

'''
The code below allows you to check the k value for each tag.
By classifying the tagss into few categories:
1. "lower": valid tags containing only lowercase letters
2. "lower_colon": valid tags with a colon in the names
3. "problemchars": tags with problematic characters
4. "other": other tags that don't fall into the 3 categories above
'''
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower,k):
            keys["lower"] += 1
        elif re.search(lower_colon,k):
            keys["lower_colon"] += 1
        elif re.search(problemchars,k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def test():
    keys = process_map('san-jose_california.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test()