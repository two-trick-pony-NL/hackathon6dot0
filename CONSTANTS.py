
OPENAI_API_KEY='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'
BUNQ_USER_API_KEY='sandbox_f1dfbb54aa005eec023ddcf6c1cdd52f2cedbd563926a1a1ae603ca6'

GENERAL_ASSISTANT_PROMPT = (
    "You are a helpful API assistant. "
    "Select the right function and fill parameters. "
    "The current time is {now}"
)
USER_ADDRESS_BOOK = (
    "Bob's email address is sugardaddy@bunq.com and we can send requests and payments there. "
    "Peter's IBAN is NL14RABO0169202917 we can only send payments here"
    "Thijs his phone number is +31612600781 and we can send requests and payments there. He does not have a email or IBAN"
    "Maurice his phone number is +31610202964 and we can send requests and payments there.  "
)
SYSTEM_ADDRESS_BOOK_PROMPT = (
    "This is the user's address book. "
    "If a name matches, attempt to use these values to fill parameters: "
)
MODEL_NAME = "gpt-4o-mini-2024-07-18"
TEXT_MODEL_NAME = "gpt-4o"
TEXT_ASSISTANT_PROMPT = (
    "You are a helpful assistant helping out with banking affairs. "
    "Assume that whatever the user requests is handled by our backend. "
    "So just confirm and be affirmative, use just a few words but do repeat some of the words so the user knows you understood the request, "
    "and mention a next step the user might take. Be funny and witty and joyful. "
    "If you get an error just ask the user to provide more details—they may have forgotten something. "
    "This is the API response: {api_response}"
)