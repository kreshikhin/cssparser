
class Attribute:
    """
    E[foo]	                Matches any E element with the "foo" attribute set (whatever the value).
    E[foo="warning"]	    Matches any E element whose "foo" attribute value is exactly equal to "warning".
    E[foo~="warning"]	    Matches any E element whose "foo" attribute value is a list of space-separated values, one of which is exactly equal to "warning".
    E[lang|="en"]           Matches any E element whose "lang" attribute has a hyphen-separated list of values beginning (from the left) with "en".
    """ 
    
    def match(self, node):
        pass   
