import unittest
import textwrap

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_link,
    text_type_image,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_simple_split(self):
        old_nodes = [TextNode("This is a **simple** test", text_type_text)]
        delimiter = "**"
        text_type = text_type_bold
        expected = [
            TextNode("This is a ", text_type_text),
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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_link(self):
        image_text = "This is text with an [link](https://www.google.com) and [another](https://www.yahoo.com)"
        result = extract_markdown_links(image_text)
        expected = [
            (
                "link",
                "https://www.google.com",
            ),
            ("another", "https://www.yahoo.com"),
        ]
        self.assertEqual(result, expected)

    def test_extract_image(self):
        image_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(image_text)
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(result, expected)


class TestMarkdownSplit(unittest.TestCase):

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
