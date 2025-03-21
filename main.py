from openai import OpenAI
import dotenv
import os


dotenv.load_dotenv()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.environ.get("ARCADE_API_KEY")
BASE_URL = os.environ.get("BASE_URL")
USER_ID = os.environ.get("USER_ID")
AVAILABLE_TOOLS = [
    "Google.SendEmail",
    "Google.SendDraftEmail",
    "Google.WriteDraftEmail",
    "Google.UpdateDraftEmail",
    "Google.DeleteDraftEmail",
    "Google.TrashEmail",
    "Google.ListDraftEmails",
    "Google.ListEmailsByHeader",
    "Google.ListEmails",
    "Google.SearchThreads",
    "Google.ListThreads",
    "Google.GetThread",
]


def call_openai(client: OpenAI, history: list[dict]):
    return client.chat.completions.create(
        messages=history,
        model=MODEL,
        user=USER_ID,
        tools=AVAILABLE_TOOLS,
        tool_choice="generate",
    )


client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

print(f"Welcome {USER_ID}. Type 'exit' to quit")
history = []
while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break

    history.append({
        "role": "user",
        "content": prompt,
    })

    try:
        response = call_openai(client, history)
        bot_content = response.choices[0].message.content

        if (
            response.choices[0].tool_authorizations
            and response.choices[0].tool_authorizations[0].get("status") == "pending"
        ):
            print(f"Bot: {bot_content}")
            input("\nPress Enter once you've authorized the app...")
            response = call_openai(client, history)
            bot_content = response.choices[0].message.content

        history.append({
            "role": "assistant",
            "content": bot_content,
        })
        print(f"Bot: {bot_content}")

    except Exception as e:
        print(f"Something went wrong: {e}")
