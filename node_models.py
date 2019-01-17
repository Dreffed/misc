from neomodel import config, StructuredRel, StructuredNode,  StringProperty, DateProperty, IntegerProperty, \
    UniqueIdProperty, RelationshipTo, RelationshipFrom

class TermRel(StructuredRel):
    rel_type = StringProperty()

class BaseNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    type = StringProperty(required = True)
    contents = StringProperty()
    wbs = StringProperty(index=True)

    connects_to = RelationshipTo('BaseNode', 'CONNECTS', model=TermRel)

class ProcessNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    type = StringProperty(required = True)
    text = StringProperty()
    wbs = StringProperty(unique_index=True, required=True)

    flow = RelationshipTo('ProcessNode', 'FLOWSTO', model=TermRel)

class AnnotateNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    text = StringProperty()
    wbs = StringProperty(unique_index=True, required=True)

    flow = RelationshipTo('ProcessNode', 'ANNOTATES', model=TermRel)

class SwimlaneNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    actor = StringProperty(required=True)
    wbs = StringProperty(unique_index=True, required=True)

    responsible = RelationshipTo('ProcessNode', 'Responsible', model=TermRel)

class PoolNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index = True, required = True)
    wbs = StringProperty(unique_index=True, required=True)

    hasactor = RelationshipTo('SwimlaneNode', 'HASACTOR', model=TermRel)

class PageNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index = True, required = True)
    wbs = StringProperty(unique_index=True, required=True)

    haspool = RelationshipTo('PoolNode', 'HASPOOL', model=TermRel)

class FileNode(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index = True, required = True)
    path = StringProperty(required = True)
    wbs = StringProperty(unique_index=True, required=True)

    contains = RelationshipTo('PageNode', 'CONTAINS', model=TermRel)



    

