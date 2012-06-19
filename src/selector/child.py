
class Child:
    """E > F	Matches any F element that is a child of an element E."""
    def __init__(self,parent,child):
        self.parent = parent
        self.child = child

    def match(self, node):
        if node.parentNode.nodeName == self.parent:
           return True
        return False
