class OnlyOfType:
    def __init__(self,element):
        self.elem = element

    def match(self,node):
        if self.elem != node.nodeName: return False
        for n in node.parentNode.childNodes:
            if self.elem==n.nodeName and node!=n : return False
        return True
