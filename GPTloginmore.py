import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Initialize the session state
st.session_state['logged_in'] = False if 'logged_in' not in st.session_state else st.session_state['logged_in']

import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Initialize the session state
st.session_state['logged_in'] = False if 'logged_in' not in st.session_state else st.session_state['logged_in']

# Define your dictionary of users and passwords
USER_CREDENTIALS = {
    os.getenv('USERNAME1'): os.getenv('PASSWORD1'),
    os.getenv('USERNAME2'): os.getenv('PASSWORD2'),
    # Add more as needed
}

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
            st.session_state["logged_in"] = True
            chatbot()
        else:
            st.warning("Incorrect Username/Password")
#... rest of the script



def chatbot():
    st.title("ChatGPT-like clone")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What is up?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    """Main function to run the app"""
    if st.session_state["logged_in"]:
        chatbot()
    else:
        login()

if __name__ == "__main__":
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
    main()


#  Local URL: http://localhost:8521
 # Network URL: http://192.168.1.119:8521
