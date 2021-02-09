from lxml import etree

from Class.Element import Element


def read_osm(filename):
    nodes = {}
    ways = {}
    relations = {}
    tree = etree.iterparse(filename, events=('start', 'end',))
    type_elem = ['node', 'way', 'relation']
    for event, elem in tree:
        if event == 'end' and elem.tag in type_elem:
            element = Element(elem.get('id'), elem.tag)
            for child in elem.getchildren():
                if child.tag == 'tag':
                    element.install_tags(child.get('k'), child.get('v'))

            if elem.tag == 'node':
                element.element.location['coordinates'] = [float(elem.get('lon')), float(elem.get('lat'))]
                nodes[element.id] = element
            if elem.tag == 'way':
                element.element.nodes = [child.get('ref') for child in elem.getchildren() if child.tag == 'nd']
                ways[element.id] = element
            if elem.tag == 'relation':
                element.element.ways = [child.get('ref') for child in elem.getchildren()
                                        if child.tag == 'member' and
                                        child.get('type') == 'way']
                element.element.outer = [child.get('ref') for child in elem.getchildren()
                                         if child.tag == 'member' and
                                         child.get('type') == 'way' and
                                         child.get('role') == 'outer']
                if len(element.element.outer) == 0:
                    element.element.outer = element.element.ways
                relations[element.id] = element
    return nodes, ways, relations
