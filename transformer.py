from CONSTANTS import OPENAI_API_KEY
from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)



def generate_text_answer(query, api_call_result):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant helping out with banking affairs. Assume that whatever the user requests is handled by our backend. So just confirm and be affirmative, use just a few words but do repeat some of the words so the user knows you understood the request, and something about a next step what would the user do next. Be funny and witty and joyfull. If you get an error just make sure to ask the user to provide more details, they may have forgotten something. This is the API response: {api_call_result}"
                },
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
