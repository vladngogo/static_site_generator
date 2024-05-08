import unittest

from inline_markdown import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_simple_split(self):
        old_nodes = [TextNode("This is **simple** test", text_type_text)]
        delimiter = "**"
        text_type = text_type_bold
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("simple", text_type_bold),
            TextNode(" test", text_type_text),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_multiple_split(self):
        old_nodes = [
            TextNode("This is a more **complex** type of **test**", text_type_text)
        ]
        delimiter = "**"
        text_type = text_type_bold
        expected = [
            TextNode("This is a more ", text_type_text),
            TextNode("complex", text_type_bold),
            TextNode(" type of ", text_type_text),
            TextNode("test", text_type_bold),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        old_nodes = [TextNode("Unmatched *delimiters", text_type_text)]
        delimiter = "*"
        text_type = text_type_bold
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_italic_split(self):
        old_nodes = [TextNode("This is an *italic* word", text_type_text)]
        delimiter = "*"
        text_type = text_type_italic
        expected = [
            TextNode("This is an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_code_split(self):
        old_nodes = [TextNode("This is a `code` word", text_type_text)]
        delimiter = "`"
        text_type = text_type_code
        expected = [
            TextNode("This is a ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" word", text_type_text),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
