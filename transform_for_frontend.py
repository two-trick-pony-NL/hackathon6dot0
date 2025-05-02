from CONSTANTS import OPENAI_API_KEY


def call_open_ai(query):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a helpful API assistant. Select the right function and fill parameters."},
                {"role": "user", "content": query}
            ],
            tools=[{"type": "function", "function": f} for f in functions],
            tool_choice="auto"
        )

        tool_call = response.choices[0].message.tool_calls[0]
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        print(f"\n→ Running {fn_name} with args {fn_args}\n")
        return call_function(fn_name, fn_args)