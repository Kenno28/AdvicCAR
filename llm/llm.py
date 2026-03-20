from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def send_user_message(user_input: str, history, context:str):
    return ""



def send_system_message(prompt:str, model:str="gpt-5-nano") -> str:
    """
    Sends a prompt to an OpenAI model and returns the generated response text.

    Args:
        prompt (str): The input text sent to the model.
        model (str, optional): The OpenAI model to use for the request.
            Defaults to "gpt-5-nano".

    Returns:
        str: The generated response text from the model.

    Raises:
        Exception: If the API request fails or no output is returned.
    """

    response = client.responses.create(
        model=model,
        input=prompt
    )

    if response.status != "completed":
        raise Exception(f"Request failed. Error: {response}")
    
    return response.output_text

def extract_car_markdown(file:str, path:str | None = None) -> str:
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
        raise Exception("File is empty!")
    
    PROMPT = f"""
    You are to create the content for a Markdown file based on the information provided below. The content is about a car. You should structure it as follows:

    Make: The make of the car
    Model: The model of the car
    Engine: The engine
    FuelType: What type of fuel is used
    Features: The car's features
    Strengths: The car's strengths
    Weaknesses: The car's weaknesses

    If you're unsure about any of the fields, leave it blank instead of adding anything except for the Make. Only add information if you're certain. Only write down the Answer in English.

    Context:
    {file}
    """

    try:
        return send_system_message(prompt=PROMPT)
    except Exception as e:
        raise Exception(f"OpenAI Response Error: {e}")