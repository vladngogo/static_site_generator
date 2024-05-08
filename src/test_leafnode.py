import unittest

from leafnode import LeafNode


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


if __name__ == "__main__":
    unittest.main()
