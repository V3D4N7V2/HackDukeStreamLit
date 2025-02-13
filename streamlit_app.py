import streamlit as st
from openai import OpenAI
import json
from urllib.parse import unquote

# Show title and description.
st.title("💬 Reciept Chatbot")
reclist = st.query_params['reclist']
json.loads(unquote(reclist))


st.write(
    "Chat with your reciepts"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:
if True:
    openai_api_key = "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"
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key, base_url="https://api.groq.com/openai/v1")

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "The user has uploaded a reciept. The user will ask questions about the reciept. The assistant will provide insights. Here is the reciept JSON: " + str(reclist)} ,
            {"role": "assistant", "content": "Hi, I'm the Reciept Chatbot. I'm here to help you with your reciept. Feel free to ask me anything!"},
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What insights can you provide?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            # model="deepseek-r1-distill-llama-70b",
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
