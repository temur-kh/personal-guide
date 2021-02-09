from Create_db.read import read
from Create_graph.create_graph import create_graph
from Parse_data.parse import parse

is_parse = False
if is_parse:
    parse()

is_read = True
if is_read:
    read()

is_create_graph = True
if is_create_graph:
    create_graph()
