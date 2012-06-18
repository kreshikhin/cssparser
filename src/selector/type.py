
class Type:
    """E	Matches any E element (i.e., an element of type E)."""
    def __init__(self,nodetype):
        self.nt=nodetype

    def match(self, node):
        if node.nodeName==self.nt:
           return True
        else:
           #print(node.nodeName)
           return False
