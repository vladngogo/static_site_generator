import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        props_to_html = node.props_to_html()
        test_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(props_to_html, test_result)


if __name__ == "__main__":
    unittest.main()
