from selector.attribute import Attribute
"""
E[foo^="bar"] An E element whose foo attribute
 value begins exactly with the string "bar"
"""

class ValueBeginst(Attribute):
    def __init__(self,elem,attr,string):
        super().__init__(attr,string,'|=')
        self.elem = elem
    def match(self,node):
        if self.elem != node.nodeName : return False
        return super().match(node)
