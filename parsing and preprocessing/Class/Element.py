from Tags.Tags import Tags
from Class.Node import Node
from Class.Relation import Relation
from Class.Way import Way
from Tags.association import roads, attractions, additionals


class Element:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.road = False
        self.important = False
        self.entrance = None
        self.name = None
        self.old_name = None
        self.tags = []
        self.global_tags = []
        self.place = {}
        self.food = {}

        if self.type == 'node':
            self.element = Node()
        if self.type == 'way':
            self.element = Way()
        if self.type == 'relation':
            self.element = Relation()

    def install_tags(self, key, value):
        if key == 'name':
            self.name = value
        elif key == 'old_name':
            self.old_name = value
        elif key == 'entrance' and value in ['yes', 'main'] and self.type == 'node':
            self.entrance = True
        else:
            if Tags.get(key) is not None:
                if Tags[key].get(value) is not None:
                    if Tags[key][value][0] in roads:
                        self.road = True
                    if Tags[key][value][0] in attractions or Tags[key][value][0] in additionals:
                        self.important = True
                    self.global_tags += Tags[key][value]
                    self.tags.append((key, value))

    def is_save(self):
        assert self.type == 'node'
        T = self.element.road['input'] > 0 and self.element.road['start_end'] > 0
        X = self.element.road['input'] > 1
        X_T = self.element.road['start_end'] > 2
        if T or X or X_T:
            self.element.road['crossroads'] = True

        self.element.save = len(self.tags) > 0 or \
                            self.element.road['crossroads'] or \
                            self.element.road['start_end'] > 0 or \
                            (self.entrance != False and self.entrance is not None and self.important)
