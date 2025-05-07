from openai import OpenAI
from CONSTANTS import (
    TEXT_MODEL_NAME,
    TEXT_ASSISTANT_PROMPT,
)

from dotenv import load_dotenv
import os

load_dotenv()  # <-- This is required to load the .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)  # <-- also make sure to pass the API key

def generate_text_answer(prompt, api_call_result):
    try:
        messages = [
            {
                "role": "system",
                "content": TEXT_ASSISTANT_PROMPT.format(api_response=api_call_result)
            },
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model = TEXT_MODEL_NAME,
            messages = messages,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
