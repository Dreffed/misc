from neomodel import (config, StructuredRel, StructuredNode,  StringProperty, DateProperty, IntegerProperty,

    UniqueIdProperty, RelationshipTo, RelationshipFrom)

class TermRel(StructuredRel):

    relType = StringProperty()

class BaseNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    type = StringProperty(required = True)
    contents = StringProperty()

    connects_to = RelationshipTo('BaseNode', 'CONNECTS', model=TermRel)


    

