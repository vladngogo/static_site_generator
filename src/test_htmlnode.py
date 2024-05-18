import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        props_to_html = node.props_to_html()
        test_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(props_to_html, test_result)

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


class TestLeafNode(unittest.TestCase):
    def test_tag_val(self):
        tag_val_node = LeafNode(tag="p", value="This is a paragraph of text")
        tag_val_result = tag_val_node.to_html()
        tag_val_test = "<p>This is a paragraph of text</p>"
        self.assertEqual(tag_val_result, tag_val_test)

    def test_with_props(self):
        tag_val_props_node = LeafNode(
            tag="a", value="Click Me!", props={"href": "https://www.google.com"}
        )
        tag_val_props_result = tag_val_props_node.to_html()
        tag_val_props_test = '<a href="https://www.google.com">Click Me!</a>'
        self.assertEqual(tag_val_props_result, tag_val_props_test)

    def test_only_val(self):
        val_node = LeafNode(value="This is just raw text")
        val_result = val_node.to_html()
        val_test = "This is just raw text"
        self.assertEqual(val_result, val_test)

    def test_tag_props(self):
        tag_props_node = LeafNode(tag="a", props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            tag_props_node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        to_html_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        test_result = to_html_node.to_html()
        test_val = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(test_result, test_val)

    def test_empty_children(self):
        empty_node = ParentNode("div", [])
        self.assertEqual(empty_node.to_html(), "<div></div>")

    def test_nested_parent_node(self):
        nested_node = ParentNode(
            "div",
            [ParentNode("p", [LeafNode("span", "Nested text")])],
        )
        self.assertEqual(
            nested_node.to_html(), "<div><p><span>Nested text</span></p></div>"
        )

    def test_with_props(self):
        node_with_props = ParentNode(
            "a", [LeafNode("span", "Click me")], {"href": "http://example.com"}
        )
        self.assertEqual(
            node_with_props.to_html(),
            '<a href="http://example.com"><span>Click me</span></a>',
        )

    def test_raises_error_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("div", "content")]).to_html()

    def test_raises_error_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()


if __name__ == "__main__":
    unittest.main()
