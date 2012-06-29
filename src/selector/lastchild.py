class LastChild:
    def __init__(self,element):
        self.elem = element
  
    def match(self,node):
        if self.elem != node.nodeName : return False
        return node == node.parentNode.lastChild
