class NthLastOfType:
    def __init__(self,element,number):
        self.elem = element
        self.n = number
        self.s=0
    def match(self,node):
        if node.nodeName != self.elem: return False
        for nd in node.parentNode.childNodes[-1::-1]:
            if nd.nodeName == node.nodeName: self.s+=1
            if nd == node and self.s == self.n: return True
        return False
        
