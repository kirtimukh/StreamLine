import json, os, dotenv
from openai import OpenAI
import streamlit as st
from tools_list import tools, available_functions

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Echo Bot", anchor="sunglasses")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def one_shot_completer(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    return completion.choices[0].message.content


def completer(messages, result=[]):
    user_prompt = messages[-1]["content"]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, tools=tools
    )

    message = completion.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]["function"]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            func_call_message = (
                f"Calling function: {function_name}({tool_call.function.arguments})"
            )

            osprompt = f"""
                Question: {user_prompt}
                RawData: {function_response}

                Using RawData answer the Question in easy to understand language. Use necessary
                formatting to make the answer more readable.
            """
            osresponse = one_shot_completer(osprompt)
            return [func_call_message, osresponse]
    else:
        return [message.content]


# React to user input
if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response_list = completer(st.session_state.messages)

    for response in response_list:
        with st.chat_message("system"):
            st.markdown(response)

        st.session_state.messages.append({"role": "system", "content": response})
