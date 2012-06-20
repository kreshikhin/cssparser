
class Adjacent():
    """Matches any F element immediately preceded by a sibling element E."""
    def __init__(self,E,F):
        self.e = E
        self.f = F
    def match(self, node):
        if node.nextSibling is None:
           return False
        if node.nextSibling.nodeName == self.e:
           return True
        return False
