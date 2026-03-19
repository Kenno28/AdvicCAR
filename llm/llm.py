import os
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