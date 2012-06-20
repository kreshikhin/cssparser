
class Adjacent():
    """Matches any F element immediately preceded by a sibling element E."""
    def __init__(self,E,F):
        self.e = E.lower()
        self.f = F.lower()
    def match(self, node):
        if node.nextSibling is None:
           return False
        if node.nextSibling.nodeName.lower() == self.e:
           return True
        return False
