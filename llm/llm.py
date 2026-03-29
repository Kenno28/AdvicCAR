from dotenv import load_dotenv
from openai import OpenAI
from retrieval.retrieve import retrieve
from openai.types.chat import ChatCompletionMessageParam
from langchain_core.documents import Document
from pydantic import BaseModel
from typing import Type
import os, json
from models.markdown_car import Markdown_Car
from models.queryrewrite import QueryRewrite
load_dotenv()
client = OpenAI()

def message(prompt:str, contexts:list[Document] | None = None, system_prompt: str| None = None, history:list[ChatCompletionMessageParam] | None = None) -> list[ChatCompletionMessageParam]:
    """
    Builds a structured list of chat messages for an LLM request based on user input,
    retrieved context, and optional conversation history.

    The function constructs a system prompt that instructs the model to evaluate whether
    a car is overpriced or fairly priced strictly based on the provided context.
    It then appends optional chat history and the current user prompt.

    Args:
        prompt (str): The user's input question or request.
        contexts (list[Document]): A list of retrieved documents containing relevant
            information. Each document must have a `page_content` attribute.
        history (list[ChatCompletionMessageParam] | None, optional): Previous conversation
            messages to maintain context. Defaults to None.

    Returns:
        list[ChatCompletionMessageParam]: A list of messages formatted for a chat-based
        LLM API, including system instructions, optional history, and the user prompt.

    Raises:
        TypeError: If `prompt` is not a string.
        ValueError: If `prompt` is empty or contains only whitespace.
    """
    if type(prompt) != str:
        raise TypeError(f"prompt type is not str. It is {type(prompt)}")

    if len(prompt.strip()) == 0:
        raise ValueError("Prompt is empty.")


    if system_prompt is None or len(system_prompt.strip()) == 0:

        context = None

        if contexts:
            context = "\n\n".join(doc.page_content for doc in contexts)

        system_prompt = f"""
        You are a helpful assistant for car-related questions.

        Based strictly on the provided context, determine whether the car is overpriced or fairly priced.
        Justify your answer and explain the strengths and weaknesses of both the car and its model.

        Be accurate and do not use any external knowledge. Only rely on the given context.
        If the context does not contain enough information, clearly state that you cannot answer.

        Relevant context:
        {context if context else ""}
        """

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt}
    ]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": prompt})
    return messages

def send_user_message(user_input: str, history: list[ChatCompletionMessageParam]|None = None, model:str="gpt-5-nano") -> str|None:
    """Sends a prompt to an OpenAI model and returns the generated response text.

    Args:
        user_input (str): The users input
        history (list[str]): history of the chat

    Returns:
        str:  Answer of the LLM
    """

    if len(user_input.strip()) == 0:
        raise ValueError("Input is empty")

    path = os.getenv("SAVE_PATH")

    if not path:
        raise EnvironmentError("Save path couldnt be found!")

    context = retrieve(user_input, path)

    messages = message(user_input, context, None, history)
        
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content



def send_system_message(prompt:str, system_prompt:str, model:str="gpt-5-nano", structure: Type[BaseModel] | None = None) -> str|BaseModel:
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
    if len(prompt.strip()) == 0 or len(system_prompt.strip()) == 0:
        raise ValueError("System Prompt or Prompt is empty.")
    

    msg = message(prompt, None, system_prompt)


    if structure is None:
        response = client.chat.completions.create(
            model=model,
            messages=msg
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("Model returned no content.")

        return content
    

    response = client.chat.completions.create(
            model=model,
            messages=msg,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": structure.__name__,
                    "schema": structure.model_json_schema(),
                },
            },
        )

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Model returned no content.")

    data = json.loads(content)
    return structure.model_validate(data)

def extract_car_markdown(content:str) -> Markdown_Car:
    """
    Creates a Markdwon Style for the Car Information. it will be used on the User´s request and to find and save cars

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
    
    if len(content) == 0:
        raise ValueError("File is empty!")
    
    SYSTEM_PROMPT = f"""
    You are to create the content for a Markdown file based on the information provided below. The content is about a car.

    If you're unsure about any of the fields, leave it blank instead of adding anything except for the Make. Only add information if you're certain. Only write down the Answer in English.
    """

    PROMPT = f"""
    INFORMATION: {content}
    """

    try:
        response = send_system_message(PROMPT, SYSTEM_PROMPT, "gpt-5-nano", Markdown_Car)

        if type(response) == Markdown_Car:
            return response
        else:
            raise TypeError("Return Vale is not Markdown Car Type")
        
    except Exception as e:
        raise Exception(f"OpenAI Response Error: {e}")
    

def rewrite_query(input:str,  model:str="gpt-5-nano") -> str|None:


    if len(input.strip()) == 0:
        raise ValueError("Input is empty")
    

    PROMPT = f"""
    Rewrite the user query for vector search.

    Return a clean keyword-based query.

    User query:
    {input}
    """

    response = client.responses.parse(
        model=model,
        input=PROMPT,
        text_format=QueryRewrite
    )

    if response.status != "completed":
        raise Exception(f"Request failed. Error: {response}")

    
    return str(response.output_parsed)