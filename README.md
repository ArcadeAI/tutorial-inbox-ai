# Inbox-AI

This tutorial shows you how to use arcade to connect your Gmail to Arcade's
[Gmail integration](https://docs.arcade.dev/toolkits/productivity/google/gmail),
allowing it to manage emails on your behalf.


# Setup

```bash
uv venv
source .venv/bin/activate
uv sync
```

# Run

Create a `.env` file and fill in these variables

```sh
ARCADE_API_KEY=arc_o1G....
OPENAI_MODEL=gpt-4o-mini
BASE_URL=https://api.arcade.dev/v1
USER_ID=<your gmail address here>
```

Then run 

```bash
python main.py
``` 

Or for the UI version:
```bash
streamlit run ui-chat.py
```
