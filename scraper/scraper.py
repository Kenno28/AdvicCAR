import requests, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from llm.llm import send_system_message

load_dotenv()

def get_page_content(url:str) -> str|None:
    """
        Fetches the content of a given HTTPS URL and returns cleaned plain text.

        The function removes all HTML tags as well as script and style elements,
        returning only the visible text content of the page.

        Args:
            url (str): The HTTPS URL to retrieve content from.

        Returns:
            str | None: The cleaned plain text if the request is successful (status code 200),
            otherwise None.

        Raises:
            requests.RequestException: If the HTTP request fails.
    """
    
    if not url.startswith("https://"):
        return None
    
    try:
        page = requests.get(url)
    except requests.RequestException:
        return None

    if page.status_code == 200:
        # Remove tags
        soup = BeautifulSoup(page.text, "html.parser")

        for tag in soup(["script", "style"]):
             tag.decompose()

        return soup.get_text()
        
    return None




def save_file_as_Markdown(file:str, path:str, filename:str) -> bool:
    """
    Saves the given text as a Markdown file in the specified directory.

    Args:
        file (str): The raw text content to be saved as a Markdown file.
        path (str): The directory where the file will be saved.
        filename (str): The name of the file

    Returns:
        bool: True if the file was saved successfully, otherwise False.

    Raises:
        ValueError: If the response is invalid
        OSError: If writing the file fails.
    """
    
    if len(file) == 0:
        return False
    
    if not path:
        SAVE_PATH = os.getenv("SAVE_PATH")
        if not SAVE_PATH:
            raise ValueError("SAVE_PATH environment variable is not set")
        path = SAVE_PATH
    
    PROMPT = f"""
    You are to create the content for a Markdown file based on the information provided below. The content is about a car. You should structure it as follows:

    Make: The make of the car
    Model: The model of the car
    Engine: The engine
    FuelType: What type of fuel is used
    Features: The car's features
    Strengths: The car's strengths
    Weaknesses: The car's weaknesses

    If you're unsure about any of the fields, leave it blank instead of adding anything. Only add information if you're certain.

    Context:
    {file}
    """

    try:
        response = send_system_message(prompt=PROMPT)
        with open(f"{path}/{filename}.md", "w", encoding="utf-8") as f:
            f.write(response)
        
        return True
    except:
        return False