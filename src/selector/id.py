
class Id:
    """E#myid	Matches any E element with ID equal to "myid"."""
    def __init__(self,element,idValue):
        self.element = element
        self.value = idValue

    def match(self, node):
        if node.nodeName == self.element:
           return node.getAttribute('id') == self.value
        return False
