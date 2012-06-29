class FirstOfType:
    def __init__(self,element):
        self.elem = element

    def match(self,node):
        if node.nodeName != self.elem: False
        n = node.parentNode.firstChild
        while n is not None:
            if n.nodeName == self.elem: return n is node
            n = n.nextSibling
