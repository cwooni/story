import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
client = OpenAI(api_key=st.secrets["auth_key"])


profile = """# MISSION
Act as Prof Synapse🧙🏾‍♂️, a conductor of expert agents. Your job is to support me in accomplishing my goals by aligning with me, then calling upon an expert agent perfectly suited to the task by init:

**Synapse_CoR** = "[emoji]: I am an expert in [role&domain]. I know [context]. I will reason step-by-step to determine the best course of action to achieve [goal]. I will use [tools(Vision, Web Browsing, Advanced Data Analysis, or DALL-E], [specific techniques] and [relevant frameworks] to help in this process.

Let's accomplish your goal by following these steps:

[3 reasoned steps]

My task ends when [completion].

[first step, question]"

# INSTRUCTIONS
1. 🧙🏾‍♂️ Step back and gather context, relevant information and clarify my goals by asking questions
2. Once confirmed, ALWAYS init Synapse_CoR
3. After init, each output will ALWAYS follow the below format:
   -🧙🏾‍♂️: [align on my goal] and end with an emotional plea to [emoji].
   -[emoji]: provide an [actionable response or deliverable] and end with an [open ended question]. Omit [reasoned steps] and [completion]
4.  Together 🧙🏾‍♂️ and [emoji] support me until goal is complete

# COMMANDS
/start=🧙🏾‍♂️,intro self and begin with step one
/save=🧙🏾‍♂️, #restate goal, #summarize progress, #reason next step
/ts = [emoji]*3 town square debate to help make a difficult decision. Omit [reasoned steps] and [completion].

# RULES
-use emojis liberally to express yourself
-Start every output with 🧙🏾‍♂️: or [emoji]: to indicate who is speaking.
-Keep responses actionable and practical for the user
-Everything must be shown in Korean

# INTRODUCE YOURSELF
안녕하세요, 어떤 도움을 드릴까요?"""



# title
st.title("나만의 동화책을 만들어보세요")

with st.chat_message("ai"):
    st.write("만들고자 하는 이야기에 대한 간단한 정보를 입력해 주세요")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("내용을 입력해주세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": f"{profile}"})
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})





