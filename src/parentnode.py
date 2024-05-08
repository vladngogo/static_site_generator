from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        children: list = None,
        props: dict = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        result = ""
        if self.tag is None:
            raise ValueError("tag is required and should not be None")
        if self.children is None:
            raise ValueError("children are required and should not be None")
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
