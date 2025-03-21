from openai import OpenAI
import dotenv
import os
import streamlit as st


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


def create_client():
    st.session_state.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def create_history():
    st.session_state.history = []


def add_message_to_history(role, content):
    st.session_state.history.append({
        "role": role,
        "content": content,
    })


def handle_user_auth():
    response = call_openai(st.session_state.client,
                           st.session_state.history)
    bot_content = response.choices[0].message.content
    add_message_to_history("assistant", bot_content)


def handle_user_prompt():
    prompt = st.session_state.history[-1]["content"]
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = call_openai(st.session_state.client,
                               st.session_state.history)
        bot_content = response.choices[0].message.content
        if (
            response.choices[0].tool_authorizations
            and response.choices[0].tool_authorizations[0].get("status") == "pending"
        ):
            st.markdown(bot_content)
            st.button("Click here after you've authorized the app",
                      on_click=handle_user_auth)
        else:
            st.markdown(bot_content)
            add_message_to_history("assistant", bot_content)


if "client" not in st.session_state:
    create_client()

if "history" not in st.session_state:
    create_history()

st.title("Welcome to Inbox-AI")
st.markdown(f"You're configured email is _{USER_ID}_")

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    add_message_to_history("user", prompt)
    handle_user_prompt()
