from dotenv import load_dotenv
from openai import OpenAI
from retrieval.retrieve import retrieve
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()
client = OpenAI()

def message(prompt:str, contexts, history:list[ChatCompletionMessageParam] | None = None) -> list[ChatCompletionMessageParam]:
    context = "\n\n".join(doc.page_content for doc in contexts)
    
    system_prompt = f"""
    You are a helpful assistant for car-related questions.

    Based strictly on the provided context, determine whether the car is overpriced or fairly priced.
    Justify your answer and explain the strengths and weaknesses of both the car and its model.

    Be accurate and do not use any external knowledge. Only rely on the given context.
    If the context does not contain enough information, clearly state that you cannot answer.

    Relevant context:
    {context}
    """

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt}
    ]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": prompt})
    return messages

def send_user_message(user_input: str, history: list[ChatCompletionMessageParam] |None = None, model:str="gpt-5-nano") -> str|None:
    """Sends a prompt to an OpenAI model and returns the generated response text.

    Args:
        user_input (str): The users input
        history (list[str]): history of the chat

    Returns:
        str:  Answer of the LLM
    """

    context = retrieve(user_input)

    print(f"Context: {context}")

    messages = message(user_input, context, history)
        
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content



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

def extract_car_markdown(file:str, path:str | None = None) -> tuple[str, str]:
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

    Title: Name of the Document
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
        response = send_system_message(prompt=PROMPT)

        title = response[response.find("Title:") + len("Title:"): response.find("\n")]

        return response, title
    except Exception as e:
        raise Exception(f"OpenAI Response Error: {e}")