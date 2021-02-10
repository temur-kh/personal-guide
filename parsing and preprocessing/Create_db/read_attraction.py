import json
import os


def read_attraction(filename, nodes, ways, relations):
    files = os.listdir(path=filename + 'features/')
    kinds = []
    for file in files:
        with open(filename + 'features/' + file, 'r', encoding='utf-8') as f:
            text = json.load(f)
        for data in text['features']:
            if data['properties'].get('osm') is not None:
                kinds += data['properties']['kinds'].split(',')
                osm = data['properties']['osm'].split('/')
                if osm[0] == 'node':
                    elem = nodes.get(osm[1])
                elif osm[0] == 'way':
                    elem = ways.get(osm[1])
                    if elem is not None:
                        if elem.entrance is not None:
                            elem = nodes[elem.entrance]
                else:
                    elem = relations.get(osm[1])
                    if elem is not None:
                        if elem.entrance is not None:
                            elem = nodes[elem.entrance]

                if elem is not None:
                    elem.place['id_place'] = data['id']
                    elem.place['rate'] = data['properties']['rate']
                    elem.place['kinds'] = data['properties']['kinds'].split(',')
                    with open(filename + 'by_id/' + data['id'] + '.json', 'r', encoding='utf-8') as f:
                        info = json.load(f)
                    if info.get('info') is not None:
                        elem.place['description'] = info['info']['descr']
                    elif info.get('wikipedia_extracts') is not None:
                        elem.place['description'] = info['wikipedia_extracts']['text']
    return nodes, ways, relations

