from os import path
from shutil import rmtree
from copystatic import copy_directory
from generate_page import generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_template = "./template.html"


def main():
    print("Deleting public dir")
    if path.exists(dir_path_public):
        rmtree(dir_path_public)

    print(f"copying static files to public dir")
    copy_directory(dir_path_static, dir_path_public)

    print(f"Generating pages...")
    generate_page_recursive(dir_path_content, dir_path_template, dir_path_public)


if __name__ == "__main__":
    main()
