"""Rule-based terminal FAQ assistant. Run with: python chatbot.py"""
import re

FAQS = [
    {
        "patterns": [r"\b(hours|timing|open|close|working hours)\b"],
        "response": "Our sample support hours are Monday-Friday, 9 AM-5 PM. (Replace this sample with your organization's real hours.)",
    },
    {
        "patterns": [r"\b(price|cost|pricing|charge|payment)\b"],
        "response": "For pricing and payment details, please check the official pricing page or contact the support team.",
    },
    {
        "patterns": [r"\b(refund|return|cancel|cancellation)\b"],
        "response": "Please share your order/reference number with the support team to check the applicable return or cancellation policy.",
    },
    {
        "patterns": [r"\b(password|login|sign in|account|locked)\b"],
        "response": "Try using the official password-reset option. Never share your password or OTP with anyone.",
    },
    {
        "patterns": [r"\b(contact|email|phone|support|human|agent)\b"],
        "response": "Please use the contact details listed on the organization's official website.",
    },
    {
        "patterns": [r"\b(hi|hello|hey|namaste)\b"],
        "response": "Hello! 😊 How can I help you today?",
    },
    {
        "patterns": [r"\b(thank you|thanks|thank)\b"],
        "response": "You're welcome! Is there anything else I can help with?",
    },
]


def get_response(message: str) -> str:
    normalized = re.sub(r"\s+", " ", message.lower()).strip()
    if not normalized:
        return "Please type a question so I can try to help."
    for faq in FAQS:
        if any(re.search(pattern, normalized) for pattern in faq["patterns"]):
            return faq["response"]
    return (
        "I'm not sure I understood that. Try asking about business hours, pricing, "
        "refunds, account login, or support contact details."
    )


def main():
    print("FAQ Assistant")
    print("Ask a question. Type 'bye', 'exit', or 'quit' to leave.")
    while True:
        try:
            message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if message.lower() in {"bye", "exit", "quit"}:
            print("Bot: Goodbye! Have a great day.")
            break
        print("Bot:", get_response(message))


if __name__ == "__main__":
    main()
