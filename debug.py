import openai
import streamlit as st
import toml


st.title("Debug")
if "counter" not in st.session_state:
    print("HHEHHEHEHE")
    st.session_state.counter = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
print("iter")
if st.session_state.counter == 0:
    print(3)
    if prompt := st.chat_input("What is up?"):
        print(1)
        st.session_state.counter = 1
        st.rerun()
else:
    if prompt := st.chat_input("What u do?"):
        print(2)
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user"):
    #     st.markdown(prompt)

    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = "hihi"

    #     message_placeholder.markdown(full_response)
    # st.session_state.messages.append({"role": "assistant", "content": full_response})
