import streamlit as st
from st_pages import Page, show_pages
from PIL import Image

import pandas as pd
import mysql.connector
from openai import OpenAI

st.set_page_config(
    page_title="물질이 뜨고 가라앉는 성질",
    page_icon="./image/alpaca.jpg",
    layout="wide"
)

image = Image.open("image/header2.jpg")
st.image(image)
st.subheader("")
st.title("학생 답안 제출 양식")
st.divider()
st.header("5문제의 서술형 답안을 제출하세요")

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

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

hints = {
    "1": "힌트: 밀도의 공식을 기억해 보세요!",
    "2": "힌트: 혼합물의 밀도는 일정한가요? 일정하지 않다면 그 이유는?",
    "3": "힌트: 밀도 = 질량/부피 니까 이를 이용해 봅시다 :)",
    "4": "힌트: 뜨고 가라앉는 현상과 밀도의 관계를 생각해 봅시다!",
    "5": "힌트: 밀도는 물질의 특성이죠?"
}

example_answers = {
    "1": "밀도란 어떤 물질의 부피를 질량으로 나눈 값이다.",
    "2": "혼합물의 밀도는 성분 물질의 혼합 비율에 따라 달라진다.",
    "3": "고체의 밀도는 0.5 이다. 부피는 24cm^3이고, 질량은 12g이므로 밀도 공식에 따라 0.5가 된다.",
    "4": "(라)이다. 물의 밀도가 1이므로, 1보다 밀도가 작은 물질은 (라)이다. 혹은, (라)의 밀도가 0.8이므로 물의 밀도보다 낮아 물에 뜨는 물질은 (라)이다.",
    "5": "(나)와 (다)이다. 밀도는 물질의 특성이므로, 밀도 값이 같은 (나)와 (다)가 같은 물질일 것으로 예상된다."
}

# 힌트 상태 초기화
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = [False] * 5

with st.form(key="Feedback_form"):
    student_id = st.text_input("**학번을 입력하세요**", placeholder="예: 1학년 1반 5번 -> 10105, 1학년 1반 30번 -> 10130)")

    # st.image("number1.jpg", caption="문제1", use_column_width=True)
    answer1 = st.text_area("**1. 밀도란 무엇인지 서술하시오.**")
    
    
    # 문제 1에 대한 힌트
    submit_button1 = st.form_submit_button(label='힌트1')
    if submit_button1:
        st.session_state.show_hints[0] = not st.session_state.show_hints[0]
    if st.session_state.show_hints[0]:
        st.write(hints["1"])

    st.image("number2.jpg", caption="문제2", use_column_width=True)
    answer2 = st.text_area("**2. 소금물의 밀도에 따른 달걀의 위치를 보고 알 수 있는 사실을 '혼합물', '밀도' 용어를 넣어 서술하시오.**")
    
    # 문제 2에 대한 힌트
    submit_button2 = st.form_submit_button(label='힌트2')
    if submit_button2:
        st.session_state.show_hints[1] = not st.session_state.show_hints[1]
    if st.session_state.show_hints[1]:
        st.write(hints["2"])

    # st.image("number3.jpg", caption="문제3", use_column_width=True)
    answer3 = st.text_area("**3. 가로 4cm, 세로 2cm, 높이 3cm인 직육면제 모양의 고체 질량을 측정하였더니, 12g이었다. 이 고체의 밀도는 몇 g/cm^3인지 과정을 포함하여 구하시오.**")
    
    # 문제 3에 대한 힌트
    submit_button3 = st.form_submit_button(label='힌트3')
    if submit_button3:
        st.session_state.show_hints[2] = not st.session_state.show_hints[2]
    if st.session_state.show_hints[2]:
        st.write(hints["3"])

    st.image("number4.jpg", caption="문제4", use_column_width=True)
    answer4 = st.text_area("**4. 표는 물질 (가)~(라)의 질량과 부피를 측정한 결과이다. (1) 물에 넣었을 때 뜨는 물질을 고르시오.**")
    
    # 문제 4에 대한 힌트
    submit_button4 = st.form_submit_button(label='힌트4')
    if submit_button4:
        st.session_state.show_hints[3] = not st.session_state.show_hints[3]
    if st.session_state.show_hints[3]:
        st.write(hints["4"])

    # st.image("number5.jpg", caption="문제5", use_column_width=True)
    answer5 = st.text_area("**5. 4번의 표를 보고, (가)~(라) 중 같은 물질일 것으로 예상되는 것을 고르고, 이유를 쓰시오.**")
    
    # 문제 5에 대한 힌트
    submit_button5 = st.form_submit_button(label='힌트5')
    if submit_button5:
        st.session_state.show_hints[4] = not st.session_state.show_hints[4]
    if st.session_state.show_hints[4]:
        st.write(hints["5"])

    submit_button = st.form_submit_button(label='제출하기')

    if submit_button:
        if len(student_id) != 5 or not student_id.isdigit():
            st.error("학번은 5자리 숫자로 입력해야 합니다. 다시 시도해 주세요.")
        elif not (answer1.strip() and answer2.strip() and answer3.strip() and answer4.strip() and answer5.strip()):
            st.error("모든 문항에 답변을 입력해 주세요.")
        else:
            feedbacks = []
            for i, (answer, example_answer) in enumerate(zip([answer1, answer2, answer3, answer4, answer5], 
                                                             [example_answers["1"], example_answers["2"], example_answers["3"], 
                                                              example_answers["4"], example_answers["5"]])):
                prompt = (f"학생 답안: {answer}\n\n"
                          f"예시 답안: {example_answer}\n\n"
                          f"채점 기준: 예시 답안과 비교하여, 학생 답안이 맞는지 확인하고, 틀린 부분이 있다면 어떤 부분을 공부해야 하는지 간단히 설명해 주세요. "
                          f"feedback을 줄 때는, 다음과 같은 양식을 따라서 답변해 주세요. 1) 정답인지 아닌지(예: 맞음, 틀림, 보완이 필요함), 2) 틀리거나 보완이 필요하다면, 예시 답안과 학생 답안을 비교하여 어떤 부분을 보완하고 공부해야 하는지 설명"
                          f"학생 답안이 예시 답안과 정확히 일치하지 않더라도, 내용이 맞다면 간단히 이유를 설명해 주세요."
                          f"학생 답안과 예시 답안을 비교할 때, 동의어와 다양한 표현을 고려하여 평가해 주세요."
                          f"현재 feedback 받는 대상은 중학생이며, 학습 내용 수준은 '이온의 정의와 이온식 작성, 전기를 통한 이온 확인 방법, 앙금 생성 반응으로 특정 이온 확인하기'를 학습한 상태임을 고려해서 수준에 맞게 답변해줘."
                          f"내용 설명은 최대 200자 이내로 요약하여 제한하고, 설명할 때 교사가 학생에게 대하듯 친절하게 설명해 주세요.")

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides feedback based on given criteria."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                feedback = response.choices[0].message.content.strip()
                feedbacks.append(feedback)

            feedback_data = pd.DataFrame(
                [
                    {
                        "student_id": student_id,
                        "number1": answer1,
                        "number2": answer2,
                        "number3": answer3,
                        "number4": answer4,
                        "number5": answer5,
                        "feedback1": feedbacks[0],
                        "feedback2": feedbacks[1],
                        "feedback3": feedbacks[2],
                        "feedback4": feedbacks[3],
                        "feedback5": feedbacks[4]
                    }
                ]
            )

            # 학생에게 피드백 보여주기
            st.subheader("제출한 답안에 대한 피드백:")
            for i in range(1, 6):
                st.write(f"문제 {i}: {feedbacks[i-1]}")

            # 기존 데이터에 새로운 데이터 추가
            for row in feedback_data.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO student_responses_3 (student_id, number1, number2, number3, number4, number5, feedback1, feedback2, feedback3, feedback4, feedback5)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    row
                )
            conn.commit()

            st.success("답안이 성공적으로 제출되었습니다!")

cursor.close()
conn.close()


# 다른 페이지 표시(side)
show_pages(
    [
        Page("app1_0.py", "복습하기", ":white_check_mark:"),
        Page("app1_1.py", "종합 평가", ":100:"),
        Page("app1_2.py", "교사용 대시보드", ":bookmark_tabs:"),
    ]
)
