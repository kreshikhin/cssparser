"""
an E element, root of the document
"""

class Root:
    def __init__(self,element):
        self.elem = element

    def match(self,node):
        if self.elem == node.nodeName:
            return node.parentNode.nodeName == '#document'
        return False
