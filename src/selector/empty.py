class Empty:
    def __init__(self,element):
        self.elem = element
    def match(self,node):
        if self.elem != node.nodeName: return False
        if node.firstChild is None: return True
        return False
