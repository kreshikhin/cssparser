from selector.readonly import ReadOnly

class Disabled(ReadOnly):
    def __init__(self,element,r='r'):
        super().__init__(element,r)
        self.attr = 'disabled'
    def match(self,node):
        return super().match(node)
