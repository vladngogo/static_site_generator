from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"Unmatched delimiter: {delimiter}")
            else:
                split_text = node.text.split(delimiter)
                for i in range(0, len(split_text)):
                    if split_text[i] == "":
                        continue
                    if i % 2 != 0:
                        new_nodes.append(
                            TextNode(text=split_text[i], text_type=text_type)
                        )
                    else:
                        new_nodes.append(
                            TextNode(text=split_text[i], text_type=text_type_text)
                        )
    return new_nodes
