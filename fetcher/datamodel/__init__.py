from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Related
from py2neo import Graph


class Sentence(GraphObject):
    __primarykey__ = "id"

    id = Property()
    content = Property()

    concepts = RelatedFrom("Concept", "MENTIONED_IN")

    def __init__(self, id, content):
        self.id = id
        self.content = content


class Concept(GraphObject):
    __primarykey__ = "name"

    # id = Property()
    name = Property()
    type = Property()
    disambiguated = Property()

    examples_of = RelatedFrom("Concept", "IS_A")
    is_a = RelatedTo(Sentence, "IS_A")
    mentioned_in = RelatedTo(Sentence, "MENTIONED_IN")
    conflicting_with = Related("Concept", "CONFLICT")

    def __init__(self, name, type, mentioned_in):
        self.name = name
        self.type = type
        self.disambiguated = False

        self.mentioned_in.add(mentioned_in)

class HearstPattern(GraphObject):
    __primarykey__ = "id"

    id = Property()
    type = Property()
    super_candidates = RelatedTo(Concept, "SUPER")
    sub_candidates = RelatedTo(Concept, "SUB")

    def __init__(self, id, type):
        self.id = id
        self.type = type

