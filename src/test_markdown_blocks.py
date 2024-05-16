import unittest
import textwrap

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown_text = textwrap.dedent(
            """\
            This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items


            """
        )
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        result = markdown_to_blocks(markdown_text)
        self.assertEqual(expected, result)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), block_type_heading)
        self.assertEqual(block_to_block_type("## Heading 2"), block_type_heading)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), block_type_code)

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type("> quote line\n> another quote line"), block_type_quote
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("* item 1\n* item 2"), block_type_unordered_list
        )
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"), block_type_unordered_list
        )
        self.assertEqual(
            block_to_block_type("* item 1\n* item 2"), block_type_unordered_list
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2"), block_type_ordered_list
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a simple paragraph."), block_type_paragraph
        )


class TestBlockToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = textwrap.dedent(
            """\
            This is **bolded** paragraph
            text in a p
            tag here

            """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = textwrap.dedent(
            """\
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with *italic* text and `code` here

            """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = textwrap.dedent(
            """\
            - This is a list
            - with items
            - and *more* items

            1. This is an `ordered` list
            2. with items
            3. and more items

            """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = textwrap.dedent(
            """\
        # this is an h1

        this is paragraph text

        ## this is an h2
        """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = textwrap.dedent(
            """\
            > This is a
            > blockquote block

            this is paragraph text

            """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
