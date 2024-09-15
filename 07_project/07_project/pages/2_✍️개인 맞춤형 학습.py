import json
import boto3
import streamlit as st
import time

# AWS Bedrock 클라이언트 생성
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

st.set_page_config(page_title="개인 맞춤형 학습", page_icon="✍️")

st.title("💬 학습봇")
st.caption("🖊️ 당신의 학습을 도와드립니다.")

# 새로고침 또는 새로 접속 시
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "지금 어떤 것을 공부하고 있나요?"}]

# 이전 메시지 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
prompt = st.chat_input("Message Bedrock...")

if prompt:
    # 한글로 대답을 요청하는 프롬프트를 내부적으로 추가
    prompt_with_instruction = f"{prompt}\n\n(위 내용을 바탕으로 답변을 한글로 작성해주세요.)"

    # 사용자 입력 프롬프트만 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Amazon Bedrock에 수정된 prompt 전송
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt_with_instruction}],
                }
            ],
        }
    )

    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body,
    )
    response_body = json.loads(response.get("body").read())
    output_text = response_body["content"][0]["text"]

    # 스트리밍 형태로 응답 출력
    st.session_state.messages.append({"role": "assistant", "content": ""})
    message_placeholder = st.chat_message("assistant").empty()

    # 스트리밍 효과를 위해 한 글자씩 출력
    for chunk in output_text:
        message_placeholder.markdown(st.session_state.messages[-1]["content"] + chunk)
        st.session_state.messages[-1]["content"] += chunk
        time.sleep(0.05)  # 각 문자 사이에 지연시간을 추가해 스트리밍 효과 구현
