# main.py
from fastapi import FastAPI, Body
from ai_api_assistant import call_ai_function

app = FastAPI()


@app.get("/")
def test():
    return {"hello":"world"}


@app.post("/send_prompt")
async def send_prompt(prompt: str = Body(..., media_type="text/plain")):
    print(prompt)
    result = call_ai_function(query=prompt)
    return result


@app.post("/for_frontend")
async def for_frontend(prompt: str = Body(..., media_type="text/plain")):
    print(prompt)
    ###
    # Do the Mashid magic
    answer = "SOMETHING HARD CODED"
    ###
    return_to_frontend = {
        'finn_answer': answer,
        'type': 'card'


    }
    return return_to_frontend

