from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="개인 맞춤형 학습", page_icon="✍️")

st.title("💬 학습봇")
st.caption("🖊️ 당신의 학습을 도와드립니다.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "지금 어떤것을 공부하고 있나요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)