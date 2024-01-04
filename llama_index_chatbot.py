#!/usr/bin/env python

#UI application
import streamlit as st
from streamlit_chat import message as st_message
import os
import openai
from llama_index.memory import ChatMemoryBuffer
from llama_index import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
os.environ['OPENAI_API_KEY']="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"
#openai.api_key = os.environ["OPENAI_API_KEY"]

def load_index(persist_directory):
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir= persist_directory)
    index = load_index_from_storage(storage_context)
    return index

index = load_index("./storage")

chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    context_prompt=(
        "You are a chatbot, able to have normal interactions about Alameda County Water department (ACWD)"
        "\nInstruction: Do not make up answers. If the question is not related to ACWD or water, DO NOT provide answers to the question and just reply - my primary function is to assist with inquiries related to the Alameda County Water District (ACWD). If you have any questions about ACWD services, please let me know, and I'll be glad to help!"
        "Here are the relevant documents about ACWD for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    ),
    verbose=False,
)

# Set up the Streamlit app
st.title("🤖 Welcome to ACWD Ninja")
st.markdown(
    """ 
    ####  🗨️ Chat with your helpful assistant ACWD Ninja 📜  
    """
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask me anything about Alameda County Water Department 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] =  ["Hey ! 👋"]

#container for the chat history and user's text input
response_container, container = st.container(), st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        # Allow the user to enter a query and generate a response
        user_input  = st.text_input(
            "**Talk with ACWD Ninja here**",
            placeholder="Talk with ACWD Ninja here",
        )
        submit_button = st.form_submit_button(label='Send')

        if user_input:
            with st.spinner(
                "Generating Answer to your Query : `{}` ".format(user_input )
            ):
                response = chat_engine.chat(user_input)
                #response = chain({"question": user_input}, return_only_outputs=True)
                answer = response.response + "<br>" + "Source :", response.source_nodes[0].metadata["url"]
                print(answer)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(response.response)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            st_message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="fun-emoji")
            st_message(st.session_state["generated"][i], key=str(i), avatar_style="croodles-neutral")







