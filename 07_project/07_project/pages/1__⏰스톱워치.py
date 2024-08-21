import streamlit as st
import time

st.set_page_config(page_title="스톱워치", page_icon="⏰")

# 스톱워치 상태를 위한 변수 초기화
if "stopwatch_running" not in st.session_state:
    st.session_state.stopwatch_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0
if "records" not in st.session_state:
    st.session_state.records = []
if "input_title" not in st.session_state:
    st.session_state.input_title = ""

# 스톱워치 시작 함수
def start_stopwatch():
    if not st.session_state.stopwatch_running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.stopwatch_running = True

# 스톱워치 정지 함수
def stop_stopwatch():
    if st.session_state.stopwatch_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.stopwatch_running = False

# 스톱워치 리셋 함수
def reset_stopwatch():
    st.session_state.elapsed_time = 0.0
    st.session_state.stopwatch_running = False

# 시간 기록 함수
def record_time(title):
    st.session_state.records.append({"title": title, "time": st.session_state.elapsed_time})

# 시간을 분:초로 변환하는 함수
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}분 {seconds:02d}초"

# UI 요소
st.title("⏰스톱워치")

# 시간 표시를 위한 빈 공간 생성
time_display = st.empty()

# 버튼 가로 정렬
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("시작"):
        start_stopwatch()

with col2:
    if st.button("정지"):
        stop_stopwatch()

with col3:
    if st.button("리셋"):
        reset_stopwatch()

# 기록 제목 입력 및 기록 저장
st.session_state.input_title = st.text_input("기록 제목 입력", value=st.session_state.input_title)
if st.button("시간 기록"):
    if st.session_state.input_title:
        record_time(st.session_state.input_title)
        st.session_state.input_title = ""  # 제목 입력 필드 초기화

# 기록된 시간 표시
st.subheader("기록된 시간")
for record in st.session_state.records:
    st.write(f"**{record['title']}**: {format_time(record['time'])}")

# 초기화면 및 스톱워치 실행 중일 때 시간 갱신
while st.session_state.stopwatch_running:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time
    formatted_time = format_time(st.session_state.elapsed_time)
    time_display.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{formatted_time}</h1>", unsafe_allow_html=True)
    time.sleep(0.1)

# 초기화면에서 시간 표시
if not st.session_state.stopwatch_running:
    formatted_time = format_time(st.session_state.elapsed_time)
    time_display.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{formatted_time}</h1>", unsafe_allow_html=True)
