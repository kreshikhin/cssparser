
class Parent:
    def __init__(self,E,F):
        self.parent = E.lower()
        self.child = F.lower()

    def match(self,node):
        if node.nodeName.lower() != self.parent: return False
        while node != None :
            if  self.child == node.nodeName.lower() : return True
            node = node.firstChild
        return False
