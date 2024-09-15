import streamlit as st
import pymysql
import pandas as pd
import datetime

# AWS RDS 설정
db_host = 'text-db.cvgowuqq2x4n.ap-northeast-2.rds.amazonaws.com'
db_user = 'user_013'
db_password = 'pw_013'
db_name = 'db_013'

# 데이터베이스 연결
def get_db_connection():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

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
    try:
        # 데이터베이스 연결
        conn = get_db_connection()
        cursor = conn.cursor()

        # 테이블 생성 (테이블이 없는 경우에만)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            title VARCHAR(255),
            content TEXT
        )
        """)
        
        # 기록 삽입
        cursor.execute("""
        INSERT INTO records (date, title, content) VALUES (%s, %s, %s)
        """, (date, title, content))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success("기록이 저장되었습니다!")

    except Exception as e:
        st.error("기록 저장 중 오류가 발생했습니다.")

# 저장된 기록 불러오기 및 표시
try:
    # 데이터베이스 연결
    conn = get_db_connection()
    query = "SELECT id, date, title, content FROM records"
    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:

        # 사용자 정의 열 이름으로 데이터프레임 표시
        # 제목을 스타일링하여 표시
        st.markdown(
            """
            <style>
            .title {
                background-color: #FFFFE0; /* 노란색 배경 */
                color: #000000; /* 검은색 글자 */
                padding: 10px;
                border-radius: 5px;
                font-size: 24px; /* 크기 조절 */
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .title .emoji {
                font-size: 28px;
            }
            </style>
            <div class="title">
                <span class="emoji">📝</span>
                저장된 기록
            </div>
            """,
            unsafe_allow_html=True
        )

        # 열 이름 변경
        df_renamed = df.rename(columns={
            'id': '인덱스',
            'date': '날짜',
            'title': '제목',
            'content': '내용'
        })

        # 인덱스를 열로 포함시키기
        df_renamed = df_renamed.reset_index(drop=True)

        # 데이터프레임 표시, 인덱스 숨기기, 가로 꽉 차게 표시
        st.dataframe(df_renamed, hide_index=True, use_container_width=True)

        # 기록 삭제 기능 추가
        record_to_delete_index = st.selectbox("삭제할 기록을 선택하세요", df.index, format_func=lambda idx: df.loc[idx, 'title'])
        
        if st.button("기록 삭제"):
            try:
                # 데이터베이스 연결
                conn = get_db_connection()
                cursor = conn.cursor()

                # 선택된 기록의 ID를 가져와서 삭제
                record_id = df.loc[record_to_delete_index, 'id']
                cursor.execute("DELETE FROM records WHERE id = %s", (record_id,))
                conn.commit()
                cursor.close()
                conn.close()

                st.success("기록이 삭제되었습니다!")
                
                # 삭제 후 데이터프레임 갱신
                df = df.drop(index=record_to_delete_index)
                
            except Exception as e:
                st.error("기록 삭제 중 오류가 발생했습니다.")
        
    else:
        st.write("저장된 기록이 없습니다.")

except Exception as e:
    # 로그에만 오류를 기록
    import logging
    logging.error(f"저장된 기록을 불러오는 중 오류가 발생했습니다: {e}")
