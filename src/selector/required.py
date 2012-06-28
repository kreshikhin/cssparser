class Required:
    def __init__(self,element,r='r'):
        self.elem = element
        self.r = r.lower()
 
    def match(self,node):
        if self.elem != node.nodeName: return False
        if self.r == 'r': return node.hasAttribute('required')
        return not node.hasAttribute('required')
       
