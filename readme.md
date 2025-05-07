
<img width="1683" alt="Screenshot 2025-05-07 at 09 40 45" src="https://github.com/user-attachments/assets/28399931-3167-4213-8a83-52df9274490b" />

# 🧠 bunq MCP (Model Context Protocol)

This project is an OpenAI-powered assistant that integrates with the **bunq API**, allowing users to send natural language prompts that are translated into actionable banking operations. This app is able to send payments and requests, schedule payments, create cards, and open bank accounts through bunq’s API.

---

# 👀 Demo 
View full demo here: https://studio.youtube.com/video/wDTXks1sZmM/edit 

## 🛠 Features

- Natural language assistant using OpenAI’s GPT model
- Supports:
  - Sending & requesting payments
  - Creating Bunq.me fundraiser links
  - Scheduling recurring payments
  - Creating new debit cards
  - Listing invoices & contracts
  - Creating new monetary accounts
- Full bunq SDK integration
- Supports tool calling (function calling)

---

## 🚀 Getting Started

### 1. Clone this repo
And add a `.env` file with the following content: 

```.env
OPENAI_API_KEY=sk-...
BUNQ_USER_API_KEY=your-sandbox-api-key
```

# 🧪 Get a Sandbox API Key
You can request a sandbox user and API key with this call:

```bash
Copy
Edit```
curl --location --request POST 'https://public-api.sandbox.bunq.com/v1/sandbox-user-person' \
--header 'Content-Type: application/json' \
--header 'User-Agent: postman' \
--data ''
```
It returns a userPerson and an API key. Grab the api_key and paste it into your .env file as BUNQ_USER_API_KEY.

🔧 Install Dependencies
```bash
pip install -r requirements.txt
```

# ▶️ Run the Server
```
uvicorn main:app --reload
```

# 🧠 Example Usage
Prompt API
```curl -X 'POST' \
  'http://localhost:8000/for_frontend' \
  -H 'accept: application/json' \
  -H 'Content-Type: text/plain' \
  -d 'Send a request for 100 euro to sugardaddy@bunq.com'```
Returns:


```{
  "request": {
    "_id_": 1502206,
    "_created": "2025-05-07 07:32:52.544501",
    "_updated": "2025-05-07 07:32:52.544501",
    "_time_responded": null,
    "_time_expiry": null,
    "_monetary_account_id": 2116816,
    "_amount_inquired": {
      "_currency": "EUR",
      "_value": "100.00"
    },
    "_amount_responded": null,
    "_status": "PENDING",
    "_description": "Payment request for 100 euros.",
    "_merchant_reference": null,
    "_user_alias_created": {
      "_display_name": "S. Nicholson",
      "_avatar": {
        "_uuid": "24b633da-007f-410a-98af-aaded56b8696",
        "_image": [
          {
            "_attachment_public_uuid": "9a91eeb2-402a-44af-a2fa-8e705245ca38",
            "_height": 1023,
            "_width": 1024,
            "_content_type": "image/png"
          }
        ],
        "_anchor_uuid": null,
        "_style": "NONE"
      },
      "_country": "NL",
      "_uuid": null,
      "_public_nick_name": null
    },
    "_user_alias_revoked": null,
    "_counterparty_alias": {
      "label_monetary_account": {
        "_iban": "NL32BUNQ2025313705",
        "_is_light": false,
        "_display_name": "Sugar Daddy",
        "_avatar": {
          "_uuid": "3fada745-8305-45ab-b8c2-09cc05a51b65",
          "_image": [
            {
              "_attachment_public_uuid": "23f17b08-9ece-4c05-8dd8-4caf2b6ef549",
              "_height": 1023,
              "_width": 1024,
              "_content_type": "image/png"
            }
          ],
          "_anchor_uuid": null,
          "_style": "NONE"
        },
        "_label_user": {
          "_uuid": "297f4374-38c5-4611-9708-71297ab56a4b",
          "_display_name": "Sugar Daddy",
          "_country": "NL",
          "_avatar": {
            "_uuid": "2971760d-ee2d-4bfb-9ea0-22cafefe85c3",
            "_image": [
              {
                "_attachment_public_uuid": "060a6f77-773f-4501-a071-f8b8093b9c72",
                "_height": 480,
                "_width": 480,
                "_content_type": "image/jpeg"
              }
            ],
            "_anchor_uuid": "297f4374-38c5-4611-9708-71297ab56a4b",
            "_style": "NONE"
          },
          "_public_nick_name": "Sugar Daddy"
        },
        "_country": "NL",
        "_bunq_me": null,
        "_swift_bic": null,
        "_swift_account_number": null,
        "_transferwise_account_number": null,
        "_transferwise_bank_code": null,
        "_merchant_category_code": null
      },
      "pointer": {
        "_type__field_for_request": null,
        "_value_field_for_request": null,
        "_name_field_for_request": null,
        "_service_field_for_request": null,
        "_name": "Sugar Daddy",
        "_type_": "IBAN",
        "_value": "NL32BUNQ2025313705"
      }
    },
    "_attachment": [],
    "_minimum_age": null,
    "_require_address": null,
    "_geolocation": null,
    "_bunqme_share_url": null,
    "_redirect_url": null,
    "_reference_split_the_bill": null,
    "_batch_id": null,
    "_scheduled_id": null,
    "_address_billing": null,
    "_address_shipping": null,
    "_want_tip": null,
    "_allow_amount_lower": null,
    "_allow_amount_higher": null,
    "_allow_bunqme": null,
    "_event_id": null
  },
  "finn_answer": "You've got it! Sending a request for 100 euro to sugardaddy@bunq.com. The sugar is in the email! You might want to check your inbox for confirmation or a sweet reply. 🍬 💸"
}

# 📂 Project Structure
bash
Copy
Edit
.
├── main.py                    # FastAPI server
├── ai_api_assistant.py        # Handles OpenAI chat + tool calls
├── transformer.py             # Converts data responses into text answers
├── functions.json             # Declares tool/function definitions for OpenAI
├── .env
├── requirements.txt
└── README.md

📌 Notes
This app is sandbox-only. Do not use it with production bunq keys unless you know what you're doing. We provide this code as is without accepting any liability for you losing funds. 

It assumes all OpenAI tools are pre-defined in functions.json.

