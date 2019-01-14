from neomodel import (config, StructuredRel, StructuredNode,  StringProperty, DateProperty, IntegerProperty,

    UniqueIdProperty, RelationshipTo, RelationshipFrom)

class TermRel(StructuredRel):
    rel_type = StringProperty()

class BaseNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    type = StringProperty(required = True)
    contents = StringProperty()

    connects_to = RelationshipTo('BaseNode', 'CONNECTS', model=TermRel)

class AnnotateNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    text = StringProperty()

    flow = RelationshipTo('ProcessNode', 'ANNOTATES', model=TermRel)

class ProcessNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    type = StringProperty(required = True)
    text = StringProperty()

    flow = RelationshipTo('ProcessNode', 'FLOWSTO', model=TermRel)

class SwimlaneNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    actor = StringProperty(required=True)

    responsible = RelationshipTo('ProcessNode', 'Responsible', model=TermRel)

class PoolNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    name = StringProperty(unique_index = True, required = True)

    hasactor = RelationshipTo('SwimlaneNode', 'HASACTOR', model=TermRel)

class PageNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    name = StringProperty(unique_index = True, required = True)

    haspool = RelationshipTo('PoolNode', 'HASPOOL', model=TermRel)

class FileNode(StructuredNode):
    uuid = UniqueIdProperty()
    id = StringProperty(unique_index=True, required=True)
    local_id  = IntegerProperty(index = True)
    name = StringProperty(unique_index = True, required = True)
    path = StringProperty(required = True)

    contains = RelationshipTo('PageNode', 'CONTAINS', model=TermRel)



    

