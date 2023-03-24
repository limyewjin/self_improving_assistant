import openai
import json
import time
from retrying import retry
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define a decorator to handle retrying on specific exceptions
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000,
       retry_on_exception=lambda exception: isinstance(exception, (openai.api_errors.APIError, TimeoutError)))
def generate_response(messages, temperature=0.0, top_p=1, max_tokens=1024):
    """
    Generate a response using OpenAI API's ChatCompletion feature.

    Args:
        messages (list): List of chat messages in the conversation. Each item is a dict with `role` (system, assistant, user) and `content`.
        temperature (float, optional): Controls the randomness of the response. Defaults to 0.5.
        top_p (float, optional): Controls the nucleus sampling. Defaults to 1.
        max_tokens (int, optional): Maximum tokens in the response. Defaults to 1024.

    Returns:
        str: The generated response from the chat model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=0,
            presence_penalty=0
        )

        message = json.loads(str(response.choices[0].message))
        return message["content"].strip()

    except openai.api_errors.APIError as api_error:
        print(f"APIError: {api_error}")
        raise

    except TimeoutError as timeout_error:
        print(f"TimeoutError: {timeout_error}")
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

