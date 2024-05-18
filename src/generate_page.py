from markdown_blocks import markdown_to_html_node
from os import makedirs, path


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("#"):
            return line[2:]
    raise Exception("No header found, all pages need a single header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()

    html_nodes = markdown_to_html_node(markdown)
    html_content = html_nodes.to_html()
    page_title = extract_title(markdown)

    html = template.replace("{{ Title }}", page_title).replace(
        "{{ Content }}", html_content
    )

    if not path.exists(dest_path):
        print(f"Creating path {dest_path}")
        makedirs(path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        print(f"writing file to {dest_path}")
        file.write(html)
