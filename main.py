from fastapi import FastAPI, Body
from ai_api_assistant import execute_prompt
from transformer import generate_text_answer

app = FastAPI()

@app.get("/")
def test():
    return {"hello":"world"}


@app.post("/send_prompt")
def send_prompt(prompt: str = Body(..., media_type="text/plain")):
    print(prompt)
    result = execute_prompt(query=prompt)
    return result


@app.post("/for_frontend")
def for_frontend(prompt: str = Body(..., media_type="text/plain")):
    print(prompt)
    ###
    # Do the Mashid magic
    result = execute_prompt(query=prompt)
    #p#rint(result)
    response = generate_text_answer(prompt, result)
    
    ###
    #finn_answer = transform_response_into_human_readable()
    return_to_frontend =  {
        "finn_answer": response,
        "attachment": False,
        "attachment_url": "https://google.com",
        # "payment": {
        #     "_id_": 12345678,
        #     "_created": "2025-05-02",
        #     "_amount": {
        #     "_currency": "EUR",
        #     "_value": "35.99"
        #     },
        #     "_description": "Dinner reimbursement",
        #     "_counterparty_alias": {
        #     "label_monetary_account": {
        #         "_display_name": "L. Brunner",
        #         "_avatar": {
        #         "_image": [
        #             {
        #             "_attachment_public_uuid": "abc-123",
        #             "_height": 1024,
        #             "_width": 1024,
        #             "_content_type": "image/png"
        #             }
        #         ]
        #         }
        #     }
        #     }
        # }
    }
    return return_to_frontend

