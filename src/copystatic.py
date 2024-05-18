from os import path, mkdir, listdir
from shutil import copy
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def copy_directory(src, dest):
    if not path.exists(src):
        logging.error(f"The source directory '{src}' does not exist")
        return
    if not path.exists(dest):
        mkdir(dest)
        logging.info(f"The destination directory '{dest}' was created.")
    else:
        logging.info(f"The destination directory '{dest}' already exists")

    for item in listdir(src):
        src_item = path.join(src, item)
        dest_item = path.join(dest, item)

        if path.isfile(src_item):
            logging.info(f"* {src_item} -> {dest_item}")
            copy(src_item, dest_item)
        else:
            copy_directory(src_item, dest_item)
