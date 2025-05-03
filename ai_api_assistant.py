from bunq.sdk.model.generated.object_ import AmountObject
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from transformer import generate_text_answer
from bunq.sdk.model.generated.endpoint import (
    BillingContractSubscriptionApiObject,
    CustomerLimitApiObject,
    InvoiceByUserApiObject,
    PaymentApiObject,
    RequestInquiryApiObject,
    MonetaryAccountBankApiObject,
    CardDebitApiObject,
    SchedulePaymentApiObject,
    BunqMeTabApiObject,
    BunqMeTabEntryApiObject,
    ScheduleApiObject,
)
from CONSTANTS import (
    OPENAI_API_KEY,
    BUNQ_USER_API_KEY,
    GENERAL_ASSISTANT_PROMPT,
    SYSTEM_ADDRESS_BOOK_PROMPT,
    USER_ADDRESS_BOOK,
    MODEL_NAME,
)
from openai import OpenAI
from datetime import datetime
import json

client = OpenAI(api_key=OPENAI_API_KEY)
api_context = ApiContext.restore("bunq_api_context.conf")
BunqContext.load_api_context(api_context)
user_context = BunqContext.user_context()


def execute_api_call(prompt, name, args=None):
    try:
        if name == "send_payment":
            payment_id = send_payment(args)
            response = PaymentApiObject.get(payment_id).value
            return generate_response(prompt, response, "payment")
        elif name == "request_payment":
            request_id = request_payment(args)
            response = RequestInquiryApiObject.get(request_id).value
            return generate_response(prompt, response, "request")
        elif name == "schedule_payment":
            scheduled_payment_id = create_scheduled_payment(args)
            response = ScheduleApiObject.get(scheduled_payment_id).value
            return generate_response(prompt, response, "schedule")
        elif name == "create_card":
            response = create_card(args)
            return generate_response(prompt, response, "card")
        elif name == "create_monetary_account":
            monetary_account_id = create_monetary_account(args)
            response = MonetaryAccountBankApiObject.get(monetary_account_id).value
            return generate_response(prompt, response, "monetary_account")
        elif name == "create_bunq_me_fundraiser_link":
            response = generate_bunq_me_link(args)
            return generate_response(prompt, response, "attachment_url")
        elif name == "get_customer_limits":
            return CustomerLimitApiObject.list().value
        elif name == "get_subscription_contracts":
            return BillingContractSubscriptionApiObject.list().value
        elif name == "list_user_invoices":
            return InvoiceByUserApiObject.list().value
        else:
            return "Something went wrong"
    except KeyError as e:
        return [f"❌ Missing required field: {str(e)}"]
    except Exception as e:
        return [f"❌ Error occurred: {str(e)}"]


def execute_prompt(prompt):
    try:
        all_function = load_all_function()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_ADDRESS_BOOK_PROMPT + str(USER_ADDRESS_BOOK)
            },
            {
                "role": "system",
                "content": GENERAL_ASSISTANT_PROMPT.format(now=datetime.now())
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        tools = [{"type": "function", "function": fn} for fn in all_function]

        response = client.chat.completions.create(
            model = MODEL_NAME,
            messages = messages,
            tools = tools,
            tool_choice = "auto"
        )

        tool_call = response.choices[0].message.tool_calls[0]
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        print(f"\n→ Running {fn_name} with args {fn_args}\n")

        return execute_api_call(prompt, fn_name, fn_args)

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

def load_all_function():
    with open("functions.json", "r") as f:
        return json.load(f)

def send_payment(args):
    payment_id = PaymentApiObject.create(
        amount = args["amount"],
        counterparty_alias = args["counterparty_alias"],
        description = args["description"],
    ).value

    return payment_id

def request_payment(args):
    request_id = RequestInquiryApiObject.create(
        amount_inquired = args["amount_inquired"],
        counterparty_alias = args["counterparty_alias"],
        description = args["description"],
        allow_bunqme = False
    ).value

    return request_id

def create_scheduled_payment(args):
    schedule = {
        "time_start": args.get("schedule").get("time_start", datetime.now()),
        "recurrence_unit": args.get("schedule").get("recurrence_unit"),
        "recurrence_size": args.get("schedule").get("recurrence_size", 1)
    }

    scheduled_payment_id = SchedulePaymentApiObject.create(
        payment = {
            "amount": args.get("payment").get("amount"),
            "counterparty_alias": args.get("payment").get("counterparty_alias"),
            "description": args.get("payment").get("description"),
        },
        schedule = schedule
    ).value

    return scheduled_payment_id

def create_card(args):
    return CardDebitApiObject.create(
        second_line = " ",
        name_on_card = user_context.user_person.display_name,
        type_ = args["type"],
        product_type = args["product_type"],
    ).value

def create_monetary_account(args):
    monetary_account_id = MonetaryAccountBankApiObject.create(
        currency = args["currency"],
    ).value

    return monetary_account_id

def generate_bunq_me_link(args):
    try:
        print("Starting generate_bunq_me_link function")

        # Create the amount object (Ensure it can accept these attributes in a constructor)
        amount_inquired = AmountObject(value=str(args["amount"]["value"]), currency=args["amount"]["currency"])

        # Check if 'redirect_url' is provided
        redirect_url = args.get("redirect_url", None)

        # Create BunqMeTab entry with the parameters passed directly
        bunq_me_tab_entry = BunqMeTabEntryApiObject(
            amount_inquired=amount_inquired,
            description=args["description"],
            redirect_url=redirect_url
        )

        print("Created BunqMeTabEntry object")

        # Create the actual BunqMeTab
        print("Calling BunqMeTabApiObject.create...")
        bunq_me_tab = BunqMeTabApiObject.create(bunq_me_tab_entry)  # Pass the object as a whole

        bunq_me_tab_id = bunq_me_tab.value  # Assuming the returned object has a 'value' attribute
        print(f"Created BunqMeTab with ID: {bunq_me_tab_id}")

        # Retrieve the created tab to get the share URL
        bunq_me_tab = BunqMeTabApiObject.get(bunq_me_tab_id).value

        # Try to access the share URL in different ways
        share_url = getattr(bunq_me_tab, "bunqme_tab_share_url", None)
        if share_url:
            print(f"Found share URL: {share_url}")
            return share_url

        # If the above fails, try to access it through the entry
        if hasattr(bunq_me_tab, "bunqme_tab_entry"):
            entry = bunq_me_tab.bunqme_tab_entry
            print(f"BunqMeTabEntry attributes: {dir(entry)}")
            share_url = getattr(entry, "share_url", None)
            if share_url:
                print(f"Found share URL in entry: {share_url}")
                return share_url

        print("Could not find share URL in the response")
        return "URL generation failed: Could not find share URL in the response"

    except Exception as e:
        print(f"Error in generate_bunq_me_link: {e}")
        return f"URL generation failed: {str(e)}"

def generate_response(prompt, response, response_type):
    return {
        response_type: response,
        "finn_answer": generate_text_answer(prompt, response)
    }