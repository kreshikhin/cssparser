"""
Match an E element whose foo attribute value is exactly
 equal to any (ASCII-range) case-permutation of bar
"""
class CaseInsensitive:
    def __init__(self,elem,attr,val):
        self.attr = attr
        self.elem = elem
        self.val = val.lower()
    def match(self,node):
        if node.nodeName != self.elem : return False
        return node.getAttribute(self.attr).lower() == self.val
