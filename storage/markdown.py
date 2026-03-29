from pathlib import Path
from typing import Type
from models.markdown_car import Markdown_Car


def save_markdown(markdown:Markdown_Car, filename:str , path:str):
    """
    Saves the given content as a Markdown (.md) file at the specified location.

    The function validates the input parameters and writes the content to a file
    using UTF-8 encoding. If the target directory does not exist, an error is raised.

    Args:
        markdown (Markdown_Car): The content to be written into the Markdown file.
        filename (str): The name of the file without extension.
        path (str): The directory path where the file should be saved.

    Raises:
        ValueError: If `markdown`, `filename`, or `path` is empty or contains only whitespace.
        NotADirectoryError: If the specified path does not exist.

    Returns:
        None
    """
    
    if len(filename.strip()) == 0:
        raise ValueError("Filename is empty")
    
    if len(path.strip()) == 0:
        raise ValueError("Path is empty")
    
    if not Path(path).exists():
        raise NotADirectoryError("Path does not exists")

    full_path = Path(path)/ f"{filename}.md"

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(markdown.model_dump_json(indent=2))


    