markdown_blocks = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items


"""


def markdown_to_blocks(markdown):
    non_empty_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip():
            non_empty_blocks.append(block.strip())
    return non_empty_blocks


print(markdown_to_blocks(markdown_blocks))
