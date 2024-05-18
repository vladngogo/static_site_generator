from markdown_blocks import markdown_to_html_node
from os import makedirs, path, listdir
from pathlib import Path


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


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in listdir(dir_path_content):
        src_item = path.join(dir_path_content, item)
        dest_item = path.join(dest_dir_path, item)

        if path.isfile(src_item):
            if src_item.endswith(".md"):
                dest_item = dest_item.replace(".md", ".html")
                generate_page(src_item, template_path, dest_item)
        else:
            generate_page_recursive(src_item, template_path, dest_item)
