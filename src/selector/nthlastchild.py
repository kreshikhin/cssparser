class NthLastChild:
    def __init__(self,element,number):
        self.elem = element
        self.n = number-1

    def match(self,node):
        if node.nodeName != self.elem : False
        self.nlist = node.parentNode.childNodes
        return self.nlist[-1::-1].index(node)==self.n
