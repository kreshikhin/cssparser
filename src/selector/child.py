
class Child:
    """E > F	Matches any F element that is a child of an element E."""
    def __init__(self,parent,child):
        self.parent = parent.lower()
        self.child = child.lower()

    def match(self, node):
        if self.child == node.nodeName.lower():
           while node is not None:
               if node.parentNode.nodeName.lower() == self.parent:
                  return True
               node = node.parentNode
        return False
