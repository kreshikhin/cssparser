
class Descendant:
    """E F	Matches any F element that is a descendant of an E element."""
    def __init__(self,parent,child):
        self.parent = parent
        self.child = child
    def match(self, node):
        while node.parentNode.nodeName!='#document':
              if node.parentNode.nodeName == self.parent:
                 return True
        return False
        
