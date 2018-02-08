# Creating the database and tables
import sqlite3
conn = sqlite3.connect('data_wrangling.sqlite')

conn.text_factory = str
cur = conn.cursor()

#Make some fresh tables using executescript()
cur.execute('''DROP TABLE IF EXISTS nodes''')
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
cur.execute('''DROP TABLE IF EXISTS ways''')
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')


cur.execute('''CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT)
''')

with open('nodes.csv','r') as nodes_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(nodes_table) # comma is default delimiter
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)


cur.execute('''CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id))
''')

with open('nodes_tags.csv','r') as nodes_tags_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(nodes_tags_table) # comma is default delimiter
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags VALUES (?, ?, ?, ?);", to_db)

cur.execute('''CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT)
''')

with open('ways.csv','r') as ways_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(ways_table) # comma is default delimiter
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways VALUES (?, ?, ?, ?, ?, ?);", to_db)

cur.execute('''CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id))
''')

with open('ways_tags.csv','r') as ways_tags_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(ways_tags_table) # comma is default delimiter
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags VALUES (?, ?, ?, ?);", to_db)

cur.execute('''CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id))
''')

with open('ways_nodes.csv','r') as ways_nodes_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(ways_nodes_table) # comma is default delimiter
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes VALUES (?, ?, ?);", to_db)

#Save changes
conn.commit()
