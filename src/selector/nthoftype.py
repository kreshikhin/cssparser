class NthOfType:
    def __init__(self,element,number):
        self.elem = element
        self.n = number
 
    def match(self,node):
        k=0
        for nod in node.parentNode.childNodes:
            if nod.nodeName == self.elem: k=k+1
            if node == nod and k == self.n: return True
        return False
