class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    # __eq__ method returns True if all the properties of two TextNode objects are equal
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    #__repr__ method returns a string representation of the TextNode object ex. TextNode(TEXT, TEXT_TYPE, URL)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
        