import re
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from parentnode import ParentNode


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    non_empty_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip():
            non_empty_blocks.append(block.strip())
    return non_empty_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    lines = block.split("\n")
    if all(line.startswith("> ") for line in lines):
        return block_type_quote
    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
        return block_type_unordered_list
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return block_type_ordered_list

    return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Line missing quote")
        qline = line.lstrip(">").strip()
        quote_lines.append(qline)
    content = " ".join(quote_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def code_to_html_node(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise ValueError("Code block malformed")
    text = block[4:-3]
    children = text_to_children(text)
    return ParentNode("code", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)
