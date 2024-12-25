import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd

# 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect('user_inputs.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        student_name TEXT,
        input1 TEXT,
        input2 TEXT
    )
''')
conn.commit()

# 페이지 설정
st.set_page_config(page_title="기후 변화와 나의 생활", layout="wide")

# 수업 차시 선택을 위한 사이드바
chapter = st.sidebar.radio(
    "수업 순서",
    ("들어가며", "1차시 기본 개념 이해", "2차시 시각화 도구로 지구 온난화 이해", "3차시 나의 생각", "교사 수업 관리")
)

if chapter == "들어가며":
    st.title("기후 변화와 나의 생활")
    image_path = 'path_to_image.jpg'
    st.image(image_path, caption='기후 변화와 나의 생활')

elif chapter == "1차시 기본 개념 이해":
    st.header("1차시 기본 개념 이해")
    st.write("""
        **기후 변화의 기본 개념에 대해 학습합니다.**
             
        기후 변화란 지구 평균 기온의 장기적인 변화를 말하며, 주로 사람 활동에 의해 발생합니다.
        여기에는 화석 연료의 사용, 산업 활동, 농업 등이 포함됩니다.
    """)

elif chapter == "2차시 시각화 도구로 지구 온난화 이해":
    st.header("2차시 시각화 도구로 지구 온난화 이해")
    st.write("""
        **지구 온난화 현황을 다양한 시각화 도구로 학습합니다.**

        다양한 시각화 도구를 사용하여 지구 온난화의 상황과 영향을 살펴봅니다.
    """)

elif chapter == "3차시 나의 생각":
    st.header("3차시 나의 생각")
    st.write("""
        **지구 온난화 해결 방법에 대한 나의 생각을 정리해봅니다.**

        학번과 성명을 입력한 후, 1번과 2번 활동을 합니다.
    """)
    student_id = st.number_input("학번을 입력합니다:", min_value=1, step=1, format="%d", key="student_id")
    student_name = st.text_input("성명을 입력합니다:", key="student_name")

    # Markdown을 사용하여 글자 크기 조정
    st.markdown("#### 1) 지구 온난화를 해결할 수 있는 방법 제안해보기:")
    user_input1 = st.text_area("여기에 입력합니다...", key="user_input1")



    st.markdown("#### 2) 민주 시민으로서 참여할 수 있는 개인의 다짐 작성해보기:")
    user_input2 = st.text_area("여기에 입력합니다...", key="user_input2")

    if st.button("제출"):
        if len(user_input1) >= 100 and len(user_input2) >= 100:
            c.execute('INSERT INTO responses (student_id, student_name, input1, input2) VALUES (?, ?, ?, ?)', 
                      (student_id, student_name, user_input1, user_input2))
            conn.commit()
            st.success("입력한 의견과 학생 정보가 제출되었습니다.")
            st.write("입력한 의견1:", user_input1)
            st.write("입력한 의견2:", user_input2)
        else:
            st.error("학번과 성명을 입력하고, 각 의견을 최소 100자 이상 입력해야 제출할 수 있습니다.")

elif chapter == "교사 수업 관리":
    st.title("교사 수업 관리")
    admin_user = st.sidebar.text_input("아이디", key="admin_user")
    admin_password = st.sidebar.text_input("비밀번호", type="password", key="admin_password")

    if admin_user == "admin" and admin_password == "admin":
        st.write("학생의 응답을 조회합니다.")
        c.execute("SELECT student_id, student_name, input1, input2 FROM responses")
        data = c.fetchall()
        df = pd.DataFrame(data, columns=["학번", "성명", "의견1", "의견2"])
        st.table(df)
    else:
        st.error("접근 권한이 없습니다. 올바른 아이디와 비밀번호를 입력하세요.")

# 데이터베이스 연결 종료
conn.close()