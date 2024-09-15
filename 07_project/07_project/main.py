import streamlit as st

st.set_page_config(
    page_title="study with me!",
    page_icon="(๑•̀∀•́ฅ ✧",
)

st.title("학습일지")
st.write("나의 성장 여정을 기록하고, :blue[더 나은 내일을 설계하세요.]" )
image="image/star.jpg"
st.image(image, width=500)

st.sidebar.markdown(
    
     """
    <style>
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    .profile-pic {
        width: 100px; /* 이미지 너비 조절 */
        height: 100px; /* 이미지 높이 조절 */
        border-radius: 50%;
        display: block;
        margin: 0 auto; /* 가운데 정렬 */
        padding-top: 10px; /* 상단 여백 추가 */
    }
    .sidebar-content {
        padding-top: 120px; /* 이미지 아래에 여백 추가 */
    }

    </style>
    <img src="https://i.pinimg.com/originals/85/81/46/858146972b351699e67a5eee97f6241b.jpg" class="profile-pic" alt="Profile Picture">
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("--------")




st.sidebar.success("study with me!")