from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


def save_markdown(markdown:str, filename:str , path:str|None = None):
    """Saves the given Content as a Markdown File

    Args:
        markdown (str): The content of the Markdown
        filename (str): Name of the File
        path (str | None, optional): Where to save the File. Defaults to None.
    """
    try:
        if not path:
            SAVE_PATH = os.getenv("SAVE_PATH")
            if not SAVE_PATH:
                raise ValueError("SAVE_PATH environment variable is not set")
            path = SAVE_PATH

        base_path = Path(path) if path else Path.cwd()
        full_path = base_path / f"{filename}.md"

        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"{markdown}")
    except Exception as e:
        raise Exception(f"Error on save. Error: {e}")
    
    