
class Attribute:
    """
    E[foo]	                Matches any E element with the "foo" attribute set (whatever the value).
    E[foo="warning"]	    Matches any E element whose "foo" attribute value is exactly equal to "warning".
    E[foo~="warning"]	    Matches any E element whose "foo" attribute value is a list of space-separated values, one of which is exactly equal to "warning".
    E[lang|="en"]           Matches any E element whose "lang" attribute has a hyphen-separated list of values beginning (from the left) with "en".
    """ 
    def __init__(self,attr,value = None,comparison ='='):
        self.attr = attr
        self.val = value
        self.comp = comparison
    def match(self, node):
        if self.comp == '~=':
            return self.val in node.getAttribute(self.attr)
        if self.comp == '|=':
            return node.getAttribute(self.attr).find(self.val)==0
        if self.val != None:
            return node.getAttribute(self.attr)==self.val
        return node.hasAttribute(self.attr)
