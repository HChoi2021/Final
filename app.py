import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from io import BytesIO

# 페이지 설정 (코드 가장 위에 위치해야 함)
st.set_page_config(page_title="기후 변화와 나의 생활", layout="wide")

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

# 수업 차시 선택을 위한 사이드바
chapter = st.sidebar.radio(
    "활동 순서",
    ("들어가며", "1.기본 개념 이해", "2.시각화 도구로 지구 온난화 이해", "3.나의 생각", "교사 수업 관리")
)

if chapter == "들어가며":
    st.title("기후 변화와 나의 생활")
    image_path = 'path_to_image.jpg'  # 이미지 파일 경로를 확인하세요
    if image_path:
        st.image(image_path, caption='기후 변화와 나의 생활')
    else:
        st.warning("이미지를 찾을 수 없습니다. 경로를 확인하세요.")

    st.markdown("""
        **(2)환경과 에너지 - 3.온실효과와 지구 온난화 단원**  
        "기후변화와 나의 생활"이라는 주제로 계획된 3차시 활동입니다.
    """, unsafe_allow_html=True)

    # HTML/CSS 스타일링
    st.markdown("""
        <style>
            .box {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            .box h4 {
                margin-top: 0;
                color: #333;
            }
            .box p {
                margin: 0;
                line-height: 1.6;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

    # 박스 형태로 각 차시 내용 표시
    st.markdown("""
        <div class="box">
            <h4>1. 기본 개념 이해</h4>
            <p>지구 온난화, 온실 가스와 온실효과, 기후 변화로 인한 여러가지 현상 및 피해 등의 개념을 다룹니다.</p>
        </div>
        <div class="box">
            <h4>2. 시각화 도구로 지구 온난화 이해</h4>
            <p>지구 온난화에 큰 영향을 주는 온실가스(이산화탄소)의 연도별 대기 함유량 변화를, 여러 자료와의 연계성을 분석할 수 있도록 시각화하여 나타내는 활동을 합니다.</p>
        </div>
        <div class="box">
            <h4>3. 나의 생각</h4>
            <p>지구 온난화 감소를 위해 할 수 있는 1. 과학적 방법과 2. 자신의 다짐을 기입하는 활동입니다.</p>
        </div>
    """, unsafe_allow_html=True)

elif chapter == "1. 기본 개념 이해":
    st.header("1. 기본 개념 이해")
    st.write("""
        **기후 변화의 기본 개념에 대해 학습합니다.**
             
        기후 변화란 지구 평균 기온의 장기적인 변화를 말하며, 주로 사람 활동에 의해 발생합니다.
        여기에는 화석 연료의 사용, 산업 활동, 농업 등이 포함됩니다.
    """)

elif chapter == "2. 시각화 도구로 지구 온난화 이해":
    st.header("2. 시각화 도구로 지구 온난화 이해")
    st.write("""
        **지구 온난화 현황을 다양한 시각화 도구로 학습합니다.**

        다양한 시각화 도구를 사용하여 지구 온난화의 상황과 영향을 살펴봅니다.
    """)

elif chapter == "3. 나의 생각":
    st.header("3. 나의 생각")
    st.write("""
        **지구 온난화 해결 방법에 대한 나의 생각을 정리해봅니다.**

        학번과 성명을 입력한 후, 1번과 2번 활동을 합니다.
    """)

    st.markdown("---")
    st.subheader("학번과 성명 입력")
    student_id = st.number_input("학번을 입력합니다:", min_value=1, step=1, format="%d", key="student_id")
    student_name = st.text_input("성명을 입력합니다:", key="student_name")

    st.markdown("---")
    st.markdown("#### 1) 지구 온난화를 해결할 수 있는 방법 제안해보기 (100자 이상 입력)")
    user_input1 = st.text_area("여기에 입력합니다...", key="user_input1")
    st.caption(f"글자 수: {len(user_input1)}")

    st.markdown("#### 2) 민주 시민으로서 참여할 수 있는 개인의 다짐 작성해보기 (100자 이상 입력)")
    user_input2 = st.text_area("여기에 입력합니다...", key="user_input2")
    st.caption(f"글자 수: {len(user_input2)}")

    if st.button("제출"):
        if not student_name.strip():
            st.error("성명을 입력하세요.")
        elif len(user_input1) >= 100 and len(user_input2) >= 100:
            c.execute('INSERT INTO responses (student_id, student_name, input1, input2) VALUES (?, ?, ?, ?)', 
                      (student_id, student_name, user_input1, user_input2))
            conn.commit()
            st.success("입력한 의견과 학생 정보가 제출되었습니다.")
        else:
            st.error("각 의견을 최소 100자 이상 입력해야 제출할 수 있습니다.")

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

        # 엑셀 파일 다운로드 기능 추가
        st.markdown("### 학생 응답 데이터 다운로드")
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Responses')
            writer.save()
            processed_data = output.getvalue()

        st.download_button(
            label="엑셀 파일 다운로드",
            data=processed_data,
            file_name="학생응답데이터.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("접근 권한이 없습니다. 올바른 아이디와 비밀번호를 입력하세요.")

# 데이터베이스 연결 종료
try:
    conn.close()
except Exception as e:
    st.error(f"데이터베이스 연결 종료 중 오류 발생: {e}")