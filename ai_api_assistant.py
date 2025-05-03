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
    RequestInquiryApiObject,
    MonetaryAccountBankApiObject,
    CardDebitApiObject,
    SchedulePaymentApiObject
)
import json
from CONSTANTS import OPENAI_API_KEY, BUNQ_USER_API_KEY, USER_ADDRESS_BOOK
from datetime import datetime
import random


client = OpenAI(api_key=OPENAI_API_KEY)
api_context = ApiContext.restore("bunq_api_context.conf")
BunqContext.load_api_context(api_context)
user_context = BunqContext.user_context()

# Function registry (tool schema definitions)
with open("functions.json", "r") as f:
    functions = json.load(f)

# Function dispatch handler
def call_function(name, args=None):
    try:
        if name == "get_customer_limits":
            return CustomerLimitApiObject.list().value

        elif name == "get_subscription_contracts":
            return BillingContractSubscriptionApiObject.list().value

        elif name == "list_user_invoices":
            return InvoiceByUserApiObject.list().value

        elif name == "order_new_card":
            print("HIT THE CARD FUNCTION")

            alias = PointerObject(
                type_=args["alias"]["type"],
                value=args["alias"]["value"]
            )
            pincode = [f"{random.randint(0, 9999):04d}" for _ in range(4)]

            pin_code_assignment = {
                "type": "PRIMARY",
                "pin_code": pincode
            }

            card_id = CardDebitApiObject.create(
                second_line=" ",
                name_on_card="",
                type_=args["type"],
                product_type="MASTERCARD",
                pin_code_assignment=[pin_code_assignment]
            ).value

            return [f"💳 Card created with ID: {card_id}"]

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
        elif name == "schedule_payment":
            # Extract the amount_value and amount_currency from args
            amount_value = args.get("amount_value")
            amount_currency = args.get("amount_currency")

            if not amount_value or not amount_currency:
                return ["❌ Missing amount details: provide both 'amount_value' and 'amount_currency'"]

            # Create AmountObject
            amount = AmountObject(
                value=amount_value,
                currency=amount_currency
            )

        if args.get("recipient_email"):
            recipient = PointerObject(
                type_="EMAIL",
                value=args["recipient_email"],
                name=args.get("recipient_name", "")
            )
        elif args.get("recipient_phone"):
            recipient = PointerObject(
                type_="PHONE_NUMBER",
                value=args["recipient_phone"],
                name=args.get("recipient_name", "")
            )
        elif args.get("recipient_iban"):
            recipient = PointerObject(
                type_="IBAN",
                value=args["recipient_iban"],
                name=args.get("recipient_name", "")
            )
        else:
            return ["❌ Missing recipient info: provide email, phone, or IBAN"]

            # Handle description and schedule
            description = args.get("description", "")
            schedule = {
                "time_start": args.get("time_start"),
                "recurrence_unit": args.get("recurrence_unit"),
                "recurrence_size": args.get("recurrence_size")
            }

            # Ensure schedule fields are present
            if not all(schedule.values()):
                return ["❌ Missing schedule details: provide time_start, recurrence_unit, and recurrence_size"]

            # Create scheduled payment
            try:
                scheduled_id = SchedulePaymentApiObject.create(
                    payment={
                        "amount": amount,
                        "counterparty_alias": recipient,
                        "description": description
                    },
                    schedule=schedule
                ).value
            except:
                print("OOPs")

        return [f"✅ Scheduled payment created with ID: {scheduled_id}"]
    except Exception as e:
        return [f"❌ Error occurred: {str(e)}"]
         
    except KeyError as e:
        return [f"❌ Missing required field: {str(e)}"]
    except Exception as e:
        return [f"❌ Error occurred: {str(e)}"]




def call_ai_function(query):
    now = datetime.now()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": f"system", "content": (
                        "This is the user's address book. "
                        "If a name matches, attempt to use these values to fill parameters: "
                        f"{USER_ADDRESS_BOOK}")},
                {"role": f"system", "content": f"You are a helpful API assistant. Select the right function and fill parameters. The current time is {now}"},
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

