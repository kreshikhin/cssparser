
class Pseudoclass:
    """
    E:first-child       Matches element E when E is the first child of its parent. 	The :first-child pseudo-class
    E:link
    E:visited 	        Matches element E if E is the source anchor of a hyperlink of which the target is not yet visited (:link) or already visited (:visited). 	The link pseudo-classes
    E:active
    E:hover
    E:focus          	Matches E during certain user actions. 	The dynamic pseudo-classes
    E:lang(c) 	        Matches element of type E if it is in (human) language c (the document language specifies how language is determined).
    """
    def __init__(self, firstChild, parent):
        self.fChild = firstChild
        self.parent = parent

    def match(self, node):
        #if node.getAttribute('href')!=''
         #  return True
        if node.previousSibling is None and node.nodeName == self.fChild:
           return node.parentNode.nodeName == self.parent 
