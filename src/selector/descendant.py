
class Descendant:
    """E F	Matches any F element that is a descendant of an E element."""
    def __init__(self,parent,child):
        self.parent = parent.lower()
        self.child = child.lower()
    def match(self, node):
        if node.nodeName.lower() == self.child:
           while node.parentNode.nodeName!='#document':
                 if node.parentNode.nodeName.lower() == self.parent:
                    return True
                 node = node.parentNode
        return False
        
