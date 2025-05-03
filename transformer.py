from openai import OpenAI
from CONSTANTS import (
    OPENAI_API_KEY,
    TEXT_MODEL_NAME,
    TEXT_ASSISTANT_PROMPT,
)
client = OpenAI(api_key=OPENAI_API_KEY)

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
