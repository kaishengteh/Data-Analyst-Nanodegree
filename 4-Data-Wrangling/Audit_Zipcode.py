'''
This code checks for zipcode whether they begin with '94' or '95' or something else
'''
OSMFILE = "san-jose_california.osm"
zip_type_re = re.compile(r'\d{5}$')

def audit_ziptype(zip_types, zipcode):
    if zipcode[0:2] != 95:
        zip_types[zipcode[0:2]].add(zipcode)
    elif zipcode[0:2] != 94:
        zip_types[zipcode[0:2]].add(zipcode)
        
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    zip_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_ziptype(zip_types,tag.attrib['v'])
    osm_file.close()
    return zip_types

zip_print = audit_zip(OSMFILE)

def test():    
    pprint.pprint(dict(zip_print))

if __name__ == '__main__':
    test()
