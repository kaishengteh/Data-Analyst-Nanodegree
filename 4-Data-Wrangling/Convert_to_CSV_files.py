'''
The code below is mostly derived from Udacity Lession 13: Case study: OpenStreetMap Data [SQL]
https://classroom.udacity.com/nanodegrees/nd002/parts/860b269a-d0b0-4f0c-8f3d-ab08865d43bf/modules/316820862075461/lessons/5436095827/concepts/54908788190923
'''
OSM_PATH = "san-jose_california.osm"
OSMFILE = "san-jose_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Terrace", "Way"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Dr": "Drive",
            "Rd": "Road"
            }

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
    
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    p=0
    
    if element.tag == 'node':
        for i in NODE_FIELDS:
            node_attribs[i] = element.attrib[i]
        for tag in element.iter("tag"):
            node_tags_attribs = {}
            temp = LOWER_COLON.search(tag.attrib['k'])
            is_p = PROBLEMCHARS.search(tag.attrib['k'])
            if is_p:
                continue
            elif temp:
                split_char = temp.group(1)
                split_index = tag.attrib['k'].index(split_char)
                type1 = temp.group(1)
                node_tags_attribs['id'] = element.attrib['id']
                node_tags_attribs['key'] = tag.attrib['k'][split_index+2:]
                node_tags_attribs['value'] = tag.attrib['v']
                node_tags_attribs['type'] = tag.attrib['k'][:split_index+1]
                if node_tags_attribs['type'] == "addr" and node_tags_attribs['key'] == "street":
                    # update street name
                    node_tags_attribs['value'] = update_name(tag.attrib['v'], mapping) 
                #elif node_tags_attribs['type'] == "addr" and node_tags_attribs['key'] == "postcode":
                #    # update post code
                #    node_tags_attribs['value'] = update_zipcode(tag.attrib['v']) 
            else:
                node_tags_attribs['id'] = element.attrib['id']
                node_tags_attribs['key'] = tag.attrib['k']
                node_tags_attribs['value'] = tag.attrib['v']
                node_tags_attribs['type'] = 'regular'
                if node_tags_attribs['type'] == "addr" and node_tags_attribs['key'] == "street":
                    # update street name
                    node_tags_attribs['value'] = update_name(tag.attrib['v'], mapping) 
                #elif node_tags_attribs['type'] == "addr" and node_tags_attribs['key'] == "postcode":
                #    # update post code
                #    node_tags_attribs['value'] = update_zipcode(tag.attrib['v']) 
            tags.append(node_tags_attribs)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        id = element.attrib['id']
        for i in WAY_FIELDS:
            way_attribs[i] = element.attrib[i]
        for i in element.iter('nd'):
            d = {}
            d['id'] = id
            d['node_id'] = i.attrib['ref']
            d['position'] = p
            p+=1
            way_nodes.append(d)
        for c in element.iter('tag'):
            temp = LOWER_COLON.search(c.attrib['k'])
            is_p = PROBLEMCHARS.search(c.attrib['k'])
            e = {}
            if is_p:
                continue
            elif temp:
                split_char = temp.group(1)
                split_index = c.attrib['k'].index(split_char)
                e['id'] = id
                e['key'] = c.attrib['k'][split_index+2:]
                e['type'] = c.attrib['k'][:split_index+1]
                e['value'] = c.attrib['v']
                if e['type'] == "addr" and e['key'] == "street":
                    e['value'] = update_name(c.attrib['v'], mapping) 
                #elif e['type'] == "addr" and e['key'] == "postcode":
                #    e['value'] = update_zipcode(c.attrib['v'])
            else:
                e['id'] = id
                e['key'] = c.attrib['k']
                e['type'] = 'regular'
                e['value'] =  c.attrib['v']
                if e['type'] == "addr" and e['key'] == "street":
                    e['value'] = update_name(c.attrib['v'], mapping) 
                #elif e['type'] == "addr" and e['key'] == "postcode":
                #    e['value'] = update_zipcode(c.attrib['v'])
            tags.append(e)
        
    return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
        
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""
    with codecs.open(NODES_PATH, 'wb') as nodes_file, \
        codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
        codecs.open(WAYS_PATH, 'wb') as ways_file, \
        codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
        codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
