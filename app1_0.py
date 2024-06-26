import streamlit as st
from PIL import Image

st.set_page_config(
        page_title="Review",
        page_icon="./image/alpaca.jpg",
        layout="wide"
)
image = Image.open("image/header2.jpg")
st.image(image)
st.subheader("")
st.title("이온에 대해 배웠던 내용:sweat_smile:")
st.header(":ballot_box_with_check: 슬라이드쇼")

# 이미지 파일 경로 리스트 (image 폴더 안의 8개의 이미지 파일)
image_files = [f"image/review{i}.jpg" for i in range(1, 9)]

# 현재 이미지 인덱스를 저장하기 위한 상태 설정
if 'index' not in st.session_state:
    st.session_state.index = 0

# 버튼을 위한 열 만들기
col1, col2 = st.columns(2)

# 이전 이미지 버튼 클릭 시 인덱스 감소
with col1:
    if st.button("이전 이미지"):
        st.session_state.index = (st.session_state.index - 1) % len(image_files)

# 다음 이미지 버튼 클릭 시 인덱스 증가
with col2:
    if st.button("다음 이미지"):
        st.session_state.index = (st.session_state.index + 1) % len(image_files)

# 이미지 표시
st.image(image_files[st.session_state.index], use_column_width=True)

