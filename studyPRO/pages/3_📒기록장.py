import streamlit as st
import pandas as pd
import datetime

# 페이지 설정
st.set_page_config(page_title="기록장", page_icon="📒")

# 앱 제목
st.title("📒기록장")

# 사용자 입력 폼
with st.form(key='entry_form'):
    date = st.date_input("날짜", value=datetime.date.today())
    title = st.text_input("제목")
    content = st.text_area("내용")
    submit_button = st.form_submit_button("저장")

# 기록 저장 및 표시
if submit_button:
    # 기록을 DataFrame에 저장
    try:
        # 기록을 CSV 파일로 저장
        df = pd.read_csv("records.csv")
    except FileNotFoundError:
        # 파일이 없으면 새로 생성
        df = pd.DataFrame(columns=["Date", "Title", "Content"])
    
    new_record = pd.DataFrame([[date, title, content]], columns=["Date", "Title", "Content"])
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_csv("records.csv", index=False)
    
    st.success("기록이 저장되었습니다!")

# 저장된 기록 불러오기 및 표시
try:
    df = pd.read_csv("records.csv")
    st.write("저장된 기록:")

    # 기록 삭제 기능 추가
    record_to_delete = st.selectbox("삭제할 기록을 선택하세요", df.index)
    if st.button("기록 삭제"):
        if not df.empty:
            df = df.drop(index=record_to_delete)
            df.to_csv("records.csv", index=False)
            st.success("기록이 삭제되었습니다!")
        else:
            st.error("삭제할 기록이 없습니다.")
    
    st.dataframe(df)

except FileNotFoundError:
    st.write("저장된 기록이 없습니다.")