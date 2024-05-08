from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # __eq__ method returns True if all the properties of two TextNode objects are equal
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    # __repr__ method returns a string representation of the TextNode object ex. TextNode(TEXT, TEXT_TYPE, URL)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(text_node):
        if text_node.text_type == text_type_text:
            return LeafNode(value=text_node.text)
        if text_node.text_type == text_type_bold:
            return LeafNode(tag="b", value=text_node.text)
        if text_node.text_type == text_type_italic:
            return LeafNode(tag="i", value=text_node.text)
        if text_node.text_type == text_type_italic:
            return LeafNode(tag="code", value=text_node.text)
        if text_node.text_type == text_type_link:
            return LeafNode(tag="a", props={"href": text_node.url})
        if text_node.text_type == text_type_image:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        else:
            raise Exception(f"invalid text type: {text_node.text_type}")
