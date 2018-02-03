import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

'''
The code below updates the unexpected street types listed in the mapping list
while keeping others unchanged.
'''
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Dr": "Drive",
            "Rd": "Road"
            }

def update_name(name, mapping):
    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
    return name

def test():
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

if __name__ == '__main__':
    test()