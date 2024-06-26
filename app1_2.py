import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(
      page_title="교사용 대시보드",
      page_icon="./image/alpaca.jpg",
      layout="wide"
)

# MySQL 연결 설정
db_config = {
    'host': st.secrets["connections"]["mysql"]["host"],
    'user': st.secrets["connections"]["mysql"]["username"],
    'password': st.secrets["connections"]["mysql"]["password"],
    'database': st.secrets["connections"]["mysql"]["database"],
    'port': st.secrets["connections"]["mysql"]["port"]
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 데이터 읽기 함수
def read_existing_data():
    query = "SELECT * FROM student_responses_3"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.column_names
    return pd.DataFrame(result, columns=columns)
existing_data = read_existing_data()

# 교사용 대시보드
st.title("교사용 대시보드")
st.divider()

password = st.text_input("비밀번호를 입력하세요", type="password")
submit_button = st.button("제출")

if submit_button:
    if password == '2179':
        st.success("비밀번호가 맞습니다. 대시보드를 확인하세요.")
        st.subheader("학생 답안 현황")

        existing_data = read_existing_data()
        if existing_data.empty:
            st.write("제출된 답안이 없습니다.")
        else:
            st.dataframe(existing_data)
    else:
        st.error("비밀번호가 틀렸습니다.")
