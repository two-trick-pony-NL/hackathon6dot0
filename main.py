from fastapi import FastAPI, Body
from ai_api_assistant import execute_prompt
from transformer import generate_text_answer

app = FastAPI()

@app.get("/")
def test():
    return {}


@app.post("/send_prompt")
def send_prompt(prompt: str = Body(..., media_type="text/plain")):
    response = execute_prompt(prompt)
    response["finn_answer"] = generate_text_answer(prompt, response)

    return response

@app.post("/for_frontend")
def for_frontend(prompt: str = Body(..., media_type="text/plain")):
    response = execute_prompt(prompt)
    response["finn_answer"] = generate_text_answer(prompt, response)

    return response

