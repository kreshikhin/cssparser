class ReadOnly:
    def __init__(self,element,ro='r'):
        self.elem = element
        self.r = ro.lower()
 
    def match(self,node):
        if self.elem != node.nodeName: return False
        if self.r == 'r': return node.hasAttribute('readonly')
        return not node.hasAttribute('readonly')
       
