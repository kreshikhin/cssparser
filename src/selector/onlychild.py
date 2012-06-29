class OnlyChild:
    def __init__(self,element):
        self.elem = element

    def match(self,node):
        if node.nodeName != self.elem: False
        return node.parentNode.lastChild == node.parentNode.firstChild
