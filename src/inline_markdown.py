import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"Unmatched delimiter: {delimiter}")
        for i, text_segment in enumerate(split_text):
            if text_segment == "":
                continue
            text_markdown_type = text_type_text if i % 2 == 0 else text_type
            split_nodes.append(
                TextNode(text=text_segment, text_type=text_markdown_type)
            )
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        orig_text = node.text
        images = extract_markdown_images(orig_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            text_section = orig_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(text_section) != 2:
                raise ValueError("Invalid markdown, image tag not closed")
            if text_section[0] != "":
                new_nodes.append(TextNode(text_section[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            orig_text = text_section[1]
        if orig_text != "":
            new_nodes.append(TextNode(orig_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        orig_text = node.text
        links = extract_markdown_links(orig_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            text_section = orig_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(text_section) != 2:
                raise ValueError("Invalid markdown, link tag not closed")
            if text_section[0] != "":
                new_nodes.append(TextNode(text_section[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            orig_text = text_section[1]
        if orig_text != "":
            new_nodes.append(TextNode(orig_text, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
