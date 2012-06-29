class LastOfType:
    def __init__(self,element):
        self.elem = element

    def match(self,node):
        if node.nodeName != self.elem: return False
        np = node.nextSibling
        while np != None:
            if np.nodeName is node.nodeName: return False
            np = np.nextSibling
        return True
