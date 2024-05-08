import unittest

from parentnode import ParentNode
from leafnode import LeafNode


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
