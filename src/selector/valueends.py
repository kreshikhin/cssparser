"""
Add E[foo$="bar"]
An E element whose foo attribute 
value ends exactly with the string bar
"""

class ValueEnds:
    def __init__(self,elem,attr,value):
        self.elem = elem
        self.attr = attr
        self.val  = value
 
    def match(self,node):
        if self.elem != node.nodeName: return False
        nga = node.getAttribute(self.attr)
        return nga.rfind(self.val) == len(nga) - len(self.val)
