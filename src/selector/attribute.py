
class Attribute:
    """
    E[foo]	                Matches any E element with the "foo" attribute set (whatever the value).
    E[foo="warning"]	    Matches any E element whose "foo" attribute value is exactly equal to "warning".
    E[foo~="warning"]	    Matches any E element whose "foo" attribute value is a list of space-separated values, one of which is exactly equal to "warning".
    E[lang|="en"]           Matches any E element whose "lang" attribute has a hyphen-separated list of values beginning (from the left) with "en".
    """ 
    def __init__(self,attr,valeu = None,comparison ='='):
        self.attr = attr
        self.val = valeu
        self.comp = comparison
    def match(self, node):
        print(node.getAttribute(self.attr))
        attrString = node.getAttribute(self.attr)
        if attrString == self.val or attrString!='' or self.comp == '|=' and attrString.find(self.attr)==0:
            return True
        return False
       
            
           
