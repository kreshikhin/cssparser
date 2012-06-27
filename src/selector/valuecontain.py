from selector.attribute import Attribute
"""
Add E[foo*="bar"]
An E element whose foo attribute 
value contains the substring bar
"""
class ValueContain(Attribute):
    def __init__(self, element, attribute, value):
        self.elem = element
        super().__init__(attribute,value,'~=')

    def match(self, node):
        return super().match(node)
