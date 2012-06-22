from selector.attribute import Attribute

class Class(Attribute):
    """DIV.warning	Language specific. (In HTML, the same as DIV[class~="warning"].) """
    def __init__(self,class_name):
        super().__init__(attr='class',valeu = class_name,comparison ='~=')
    def match(self, node):
        return super().match(node)

