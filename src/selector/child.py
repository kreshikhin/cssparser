
class Child:
    """E > F	Matches any F element that is a child of an element E."""
    def __init__(self,parent,child):
        self.parent = parent.lower()
        self.child = child

    def match(self, node):
        if node.parentNode.nodeName.lower() == self.parent:
           return True
        return False
