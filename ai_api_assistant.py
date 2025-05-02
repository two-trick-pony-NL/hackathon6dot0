from openai import OpenAI
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq.sdk.model.generated.endpoint import (
    BillingContractSubscriptionApiObject,
    CustomerLimitApiObject,
    InvoiceByUserApiObject,
    InvoiceExportPdfApiObject,
    InvoiceExportPdfContentApiObject,
    PaymentApiObject,
    RequestInquiryApiObject
)
import json
from CONSTANTS import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
api_context = ApiContext.restore("bunq_api_context.conf")
BunqContext.load_api_context(api_context)
user_context = BunqContext.user_context()

# Function registry (tool schema definitions)
with open("functions.json", "r") as f:
    functions = json.load(f)

# Function dispatch handler
def call_function(name, args=None):
    if name == "get_customer_limits":
        return CustomerLimitApiObject.list().value
    elif name == "get_subscription_contracts":
        return BillingContractSubscriptionApiObject.list().value
    elif name == "list_user_invoices":
        return InvoiceByUserApiObject.list().value

    elif name == "get_invoice_pdf_content":
        return ["[Binary PDF content fetched]"]
    elif name == "request_money":
        print(args["counterparty_alias"])
        return [RequestInquiryApiObject.create(
            amount_inquired=args["amount_inquired"],
            counterparty_alias=args["counterparty_alias"],
            description=args["description"],
            allow_bunqme=False
        ).value]
    elif name == "create_payment":
        amount = AmountObject(value=args["amount_value"], currency=args["amount_currency"])
        recipient = PointerObject(type_="IBAN", value=args["recipient_iban"], name=args["recipient_name"])
        description = args["description"]
        return [f"✅ Payment created with ID: {PaymentApiObject.create(amount, recipient, description).value}"]
    else:
        raise ValueError(f"Unknown function: {name}")



def call_ai_function(query):
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

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

