import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from io import BytesIO
from datetime import datetime  # 날짜 및 시간 모듈 추가
from PIL import Image
import base64
import json  # JSON 모듈 추가
import matplotlib.pyplot as plt
import mplcursors



# 페이지 설정 (코드 가장 위에 위치해야 함)
st.set_page_config(page_title="기후 변화와 나의 생활", layout="wide")

# 세션 상태 초기화
if "chapter" not in st.session_state:
    st.session_state.chapter = "들어가며"

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False    

st.markdown(
    """
    <style>
    body {
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)    

# 데이터베이스 연결 및 테이블 생성
db_path = 'user_inputs.db'
with sqlite3.connect(db_path) as conn:
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            student_id INTEGER,
            student_name TEXT,
            chapter TEXT,
            answers TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()

# 이미지 경로 혹은 URL
image_path = "Hyundai_en.png"  # 로컬 파일 경로
img = Image.open(image_path)

# 이미지 크기 조정 (예: 너비 150px, 비율에 맞게 높이 조정)
new_width = 90
new_height = int(new_width * (img.height / img.width))
img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# 이미지를 바이트 배열로 변환
buffer = BytesIO()
img_resized.save(buffer, format="PNG")
img_byte = buffer.getvalue()

# 바이트 데이터를 Base64 문자열로 인코딩
encoded_img = base64.b64encode(img_byte).decode('utf-8')

# 사이드바에 HTML을 사용하여 이미지 가운데 정렬
st.sidebar.markdown(
    f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded_img}"></div>',
    unsafe_allow_html=True
)

# 제목의 마진을 CSS로 조정하여 이미지와의 간격을 줄입니다
st.sidebar.markdown(
    '<h1 style="text-align: center; font-size: 12px; margin-top: -20px;">생명과학 최호진T</h1>',
    unsafe_allow_html=True
)

# 사이드바 설정
chapter_order = ["들어가며", "1.기본 개념 이해", "2.시각화 도구로 지구 온난화 이해", "3.나의 생각", "교사 수업 관리"]
chapter = st.sidebar.radio("<활동 순서>", chapter_order, index=chapter_order.index(st.session_state.chapter if "chapter" in st.session_state else "들어가며"))

# 사이드바에 폼 추가
with st.sidebar:
    with st.form(key='login_form'):
        admin_user = st.text_input("아이디", key="admin_user")
        admin_password = st.text_input("비밀번호", type="password", key="admin_password")
        submit_button = st.form_submit_button("로그인")

    if submit_button:
        if admin_user == "admin" and admin_password == "admin":
            st.session_state.is_admin = True
            st.sidebar.success("로그인 성공")      
        else:
            st.session_state.is_admin = False
            st.error("접근 권한이 없습니다. 올바른 아이디와 비밀번호를 입력하세요.")

# 버튼 추가 함수 정의
def next_chapter_button(current_chapter):
    if st.button("다음 챕터로 이동"):
        next_chapter_index = chapter_order.index(current_chapter) + 1
        if next_chapter_index < len(chapter_order):
            st.session_state.chapter = chapter_order[next_chapter_index]
            st.rerun()
        else:
            st.warning("더 이상 다음 챕터가 없습니다.")

# 페이지 내용 구성
if chapter == "들어가며":
    st.markdown('<h1 style="color: green;">기후 변화와 나의 생활</h1>', unsafe_allow_html=True)
    image_path = 'path_to_image.jpg'
    img = Image.open(image_path)
    new_width = 500
    new_height = int(new_width * (img.height / img.width))
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    st.image(img_resized, caption="기후 변화와 나의 생활 영향은?")

    st.markdown("""
        **(2)환경과 에너지 - 3.온실효과와 지구 온난화 단원**  
        "기후변화와 나의 생활"이라는 주제로 계획된 3차시 활동입니다.
    """, unsafe_allow_html=True)

    chapters = [
        ("1.기본 개념 이해", "지구 온난화, 온실 가스와 온실효과, 기후 변화로 인한 여러 가지 현상 및 피해 등의 개념을 다룹니다."),
        ("2.시각화 도구로 지구 온난화 이해", "지구 온난화에 큰 영향을 주는 온실가스(이산화탄소)의 연도별 대기 함유량 변화를, 여러 자료와의 연계성을 분석할 수 있도록 시각화하여 나타내는 활동을 합니다."),
        ("3.나의 생각", "지구 온난화 감소를 위해 할 수 있는 1. 과학적 방법과 2. 자신의 다짐을 기입하는 활동입니다.")
    ]

    # CSS 스타일링과 HTML 코드를 포함
    st.markdown("""
        <style>
            .box {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f0ffff;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .box:hover {
                background-color: #e8e8e8;
            }
            .blue-text {
                color: blue !important;
            }
        </style>
    """, unsafe_allow_html=True)

    for chapter_name, description in chapters:
        col1, col2 = st.columns([3, 1])
        with col1:
            # 특정 챕터 제목에 대한 스타일 조건적 적용
            if chapter_name == "2.시각화 도구로 지구 온난화 이해":
                title_style = "blue-text"
            else:
                title_style = ""

            st.markdown(f"""
                <div class="box">
                    <h4 class="{title_style}">{chapter_name}</h4>
                    <p>{description}</p>
                </div>
            """, unsafe_allow_html=True)
 
        with col2:
            if st.button("이동(2번 클릭)", key=chapter_name):
                st.session_state.chapter = chapter_name

elif chapter == "1.기본 개념 이해":
    st.header("1.기본 개념 이해")
    st.write("""
        **기후 변화의 기본 개념에 대해 학습합니다.**
             
        기후 변화란 지구 평균 기온의 장기적인 변화를 말하며, 주로 사람 활동에 의해 발생합니다.
        여기에는 화석 연료의 사용, 산업 활동 등이 포함됩니다.
    """)

    # 소제목 및 설명
    st.header("(1) 지구 온난화")
    st.image("global-warming2.png", caption="지구 온난화 현상")
    st.write("""
    지구 온난화는 지구의 평균 기온이 인간 활동의 결과로 점진적으로 상승하는 현상입니다. 
    이는 주로 화석 연료의 연소, 산업 활동, 농업 및 삼림 벌채와 같은 활동에서 발생하는 온실 가스의 증가 때문입니다.
    """)

    st.image("what-is-global-warming.png", caption="지구 온난화 원인")

    # 추가적인 리소스 링크 제공
    st.subheader("추가 정보")
    st.write("더 많은 정보를 원하면 다음 링크를 방문합니다.")
    st.markdown("[지구 온난화에 대한 정보](https://dailyinfographic.com/what-causes-global-warming)")

    # 온실 가스와 온실효과
    st.header("(2) 온실가스와 온실효과")
    st.image("greenhouse.gif", caption="온실가스와 온실효과")
    st.write("""
    온실가스는 지구의 대기 중에 존재하며, 태양으로부터 오는 복사 에너지를 흡수하고 방출하여 지구의 온도를 조절하는 역할을 합니다.
    주요 온실가스에는 이산화탄소, 메탄, 아산화질소 등이 있습니다. 이 가스들은 지구에서 태양으로부터 받은 열이 우주로 빠져나가는 것을 방해하여,
    지구의 온도를 상승시키는 온실효과를 유발합니다.
    """)

    st.image("What-Are-Some-Common-GHGs-Infographic-Final.jpg", caption="온실가스")
    st.image("Greenhouse-Effect-Infographic-Final.jpg", caption="온실효과")

    # 추가적인 리소스 링크 제공
    st.subheader("추가 정보")
    st.write("더 많은 정보를 원하면 다음 링크를 방문합니다.")
    st.markdown("[온실효과에 대한 정보](https://science.nasa.gov/climate-change/faq/what-is-the-greenhouse-effect/")
    st.markdown("[온실가스에 대한 정보](https://www.musimmas.com/resources/blogs/what-are-greenhouse-gases-ghgs-and-how-do-they-cause-climate-change/")
    st.markdown("[온실효과에 대한 정보](https://www.columbia.edu/~vjd1/greenhouse.htm")
 
    # 그래프와 데이터 시각화
    st.header("(3) 기후 변화로 인한 현상 및 피해")
    st.image("b1.jpg", caption="기후 변화로 인한 현상 및 피해")
    st.write("""
    기후 변화는 다양한 자연 재해의 증가, 해수면 상승, 생태계 변화 등 다양한 글로벌 문제를 초래합니다.
    이러한 변화는 인류의 생활 방식과 환경에 직접적인 영향을 미치며, 이에 대한 이해와 대응이 필요합니다.
    """)

    st.image("a1.png", caption="기상이변 발생 건수(시기별 및 지역별)")
    st.image("a2.png", caption="기상이변에 따른 경제적 손실")

    st.subheader("추가 정보")
    st.write("더 많은 정보를 원하면 다음 링크를 방문합니다.")
    st.markdown("[국제 사회의 기상이변 정보](https://www.ifs.or.kr/bbs/board.php?bo_table=News&wr_id=53684")

    # 사용자 입력 받기
    st.subheader("(4) 생각 정리하기")
    # 학생 정보 입력 받기
    student_id = st.number_input("학번을 입력합니다:", min_value=1, step=1, format="%d")
    student_name = st.text_input("성명을 입력합니다:")
    input1 = st.text_area("가. 지구 온난화의 원인은 무엇이라고 생각하나요?")
    input2 = st.text_area("나. 온실가스는 무슨 종류가 있고, 어떤 역할을 하나요?")
    input3 = st.text_area("다. 지구 온난화로 인해 피해와 불편함에는 무엇이 있을까요?")

    if st.button("제출"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        answers = {"input1": input1, "input2": input2, "input3": input3}
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            chapter = "1.기본 개념 이해"  # 현재 챕터 값 설정
            c.execute('''
                INSERT INTO responses (student_id, student_name, chapter, answers, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, student_name, chapter, json.dumps(answers), timestamp))
            conn.commit()
        st.success("응답이 저장되었습니다.")

    next_chapter_button("1.기본 개념 이해")


elif chapter == "2.시각화 도구로 지구 온난화 이해":
    st.header("2.시각화 도구로 지구 온난화 이해")
    st.write("""
        **지구 온난화 현황을 다양한 시각화 도구로 학습합니다.**

        자신이 직접 다양한 시각화 도구를 조합해 사용하며 지구 온난화의 상황과 영향을 살펴봅니다.
    """)

    st.header("(1) 연도별 지구 평균온도 변화")

    # 데이터 불러오기
    file_path = '01.xlsx'
    data = pd.read_excel(file_path, engine='openpyxl')  # 엔진을 openpyxl로 지정

    # 'Year'와 'Temperature Change' 열을 정의
    years = data['Year']  # 'Year' 열 이름에 맞추어 수정
    temp_changes = data['평균온도 변화(섭씨온도)']  # 'Temperature Change' 열 이름에 맞추어 수정

    # DataFrame으로 결합
    df = pd.DataFrame({'Year': years, '평균온도 변화(섭씨온도)': temp_changes}).dropna()

    # 다시 years와 temp_changes 정의
    years = df['Year'].tolist()
    temp_changes = df['평균온도 변화(섭씨온도)'].tolist()

    # 길이 확인
    if len(years) != len(temp_changes):
        st.error("연도와 온도 변화 데이터의 길이가 일치하지 않습니다.")
    else:
        # 한글 폰트 설정
        plt.rc('font', family='NanumGothic')
        plt.rc('axes', unicode_minus=False)
        
        plt.figure(figsize=(10, 5))  # 그래프 크기 설정
        line = plt.plot(years, temp_changes, marker='o', linestyle='-', color='b', label='온도 변화')  # unpacking the line
        plt.axhline(0, color='red', linestyle='--', linewidth=1)  # 기준선 추가
        plt.title('Global Average Temperature Change Over Time')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature Change (°C)')
        plt.grid(True)
        
        # mplcursors를 사용하여 데이터 레이블 표시
        mplcursors.cursor(line, hover=True)

        st.pyplot(plt)  # Streamlit에 그래프 표시

    # 데이터베이스 경로 설정
    db_path = 'responses.db'

    # 데이터베이스 연결 및 테이블 생성
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                student_id INTEGER,
                student_name TEXT,
                chapter TEXT,
                answers TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()

    # 학생 정보 입력 받기
    st.header("(2) 연도별 지구 평균온도 변화에 대한 나의 생각")

    student_id = st.number_input("학번을 입력합니다:", min_value=1, step=1, format="%d")
    student_name = st.text_input("성명을 입력합니다:")
    input1 = st.text_area("가. 1880년부터 연도별로 지구 평균 온도는 어떻게 변화하고 있나요?")
    input2 = st.text_area("나. 1980년부터 지구 평균 온도는 어떻게 변화하고 있나요?")
    input3 = st.text_area("다. 그 이유는 무엇이라고 생각하나요?")

    if st.button("제출"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        answers = {
            "input1": input1,
            "input2": input2,
            "input3": input3
        }
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            chapter = "1. 기본 개념 이해"  # 현재 챕터 값 설정
            c.execute('''
                INSERT INTO responses (student_id, student_name, chapter, answers, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, student_name, chapter, json.dumps(answers), timestamp))
            conn.commit()
        st.success("응답이 저장되었습니다.")


    # 데이터 불러오기
    file_path = '02.xlsx'
    data = pd.read_excel(file_path, engine='openpyxl', header=0)  # 첫 번째 행을 헤더로 설정

    # 데이터 전처리
    data.columns = data.columns.str.strip()  # 열 이름의 공백 제거
    data.set_index('Year', inplace=True)  # 'Year' 열을 인덱스로 설정
    data = data.apply(pd.to_numeric, errors='coerce')  # 숫자로 변환

    st.header("(3) 안면도의 온실가스량 변화")

    # 데이터 구조 확인 (디버깅용)
    st.write(data)

    # 전체 그래프 vs 개별 그래프 선택
    show_all = st.radio("그래프 보기 옵션", ("개별 온실가스", "전체 온실가스"))

    if show_all == "개별 온실가스":
        # 온실가스 종류 옵션
        gas_options = data.columns.tolist()  # 열 이름(온실가스 종류)
        selected_gas = st.selectbox("온실가스 선택", gas_options)

        # 그래프 그리기
        st.header(f"안면도 온실가스 {selected_gas} 연도별 현황")
        plt.figure(figsize=(10, 5))

        if selected_gas in data.columns:
            plt.plot(data.index, data[selected_gas], marker='o', label=selected_gas)
            plt.title(f"안면도 온실가스 {selected_gas} 연도별 현황")
            plt.xlabel("연도")
            plt.ylabel(f"{selected_gas} 농도")
            plt.grid()
            plt.legend()
            plt.tight_layout()  # 그래프 간격 조정
            st.pyplot(plt)
        else:
            st.error(f"{selected_gas}의 데이터가 없습니다.")

    else:
        # 전체 그래프 그리기
        st.header("안면도 온실가스")  # 그래프 제목 변경
        plt.figure(figsize=(10, 5))

        for gas in data.columns:
            plt.plot(data.index, data[gas], marker='o', label=gas)

        plt.title("안면도 온실가스")  # 그래프 제목
        plt.xlabel("연도")
        plt.ylabel("농도")
        plt.grid()
        plt.legend()
        plt.tight_layout()  # 그래프 간격 조정
        st.pyplot(plt)


    st.header("(4) 고산의 온실가스량 변화")
    # 데이터 불러오기
    file_path = '03.xlsx'
    data = pd.read_excel(file_path, engine='openpyxl', header=0)  # 첫 번째 행을 헤더로 설정

    # 데이터 전처리
    data.columns = data.columns.str.strip()  # 열 이름의 공백 제거
    data.set_index('Year', inplace=True)  # 'Year' 열을 인덱스로 설정
    data = data.apply(pd.to_numeric, errors='coerce')  # 숫자로 변환

    # 데이터 구조 확인 (디버깅용)
    st.write(data)

    # 전체 그래프 vs 개별 그래프 선택
    show_all = st.radio("그래프 보기 옵션", ("개별 온실가스", "전체 온실가스"), key="gas_option")

    if show_all == "개별 온실가스":
        # 온실가스 종류 옵션
        gas_options = data.columns.tolist()  # 열 이름(온실가스 종류)
        selected_gas = st.selectbox("온실가스 선택", gas_options, key="selected_gas")

        # 그래프 그리기
        st.header(f"고산 {selected_gas} 연도별 현황")
        plt.figure(figsize=(10, 5))

        if selected_gas in data.columns:
            plt.plot(data.index, data[selected_gas], marker='o', label=selected_gas)
            plt.title(f"고산 {selected_gas} 연도별 현황")
            plt.xlabel("연도")
            plt.ylabel(f"{selected_gas} 농도")
            plt.grid()
            plt.legend()
            plt.tight_layout()  # 그래프 간격 조정
            st.pyplot(plt)
        else:
            st.error(f"{selected_gas}의 데이터가 없습니다.")

    else:
        # 전체 그래프 그리기
        st.header("온실가스 연도별 현황")  # 그래프 제목 변경
        plt.figure(figsize=(10, 5))

        for gas in data.columns:
            plt.plot(data.index, data[gas], marker='o', label=gas)

        plt.title("온실가스 연도별 현황")  # 그래프 제목
        plt.xlabel("연도")
        plt.ylabel("농도")
        plt.grid()
        plt.legend()
        plt.tight_layout()  # 그래프 간격 조정
        st.pyplot(plt)



    next_chapter_button("2.시각화 도구로 지구 온난화 이해")


elif chapter == "3.나의 생각":
    st.header("3.나의 생각")
    st.write("""
        **지구 온난화 감소소 방법에 대한 나의 생각을 정리해봅니다.**

        학번과 성명을 입력한 후, 1번과 2번 활동을 합니다.
    """)

    st.markdown("---")
    st.subheader("학번과 성명 입력")
    student_id = st.number_input("학번을 입력합니다:", min_value=1, step=1, format="%d", key="student_id")
    student_name = st.text_input("성명을 입력합니다:", key="student_name")

    st.markdown("---")
    st.markdown("#### 1) 지구 온난화를 감소시킬 수 있는 방법 제안해보기 (100자 이상 입력)")
    user_input1 = st.text_area("여기에 입력합니다...", key="user_input1")
    st.caption(f"글자 수: {len(user_input1)}")

    st.markdown("#### 2) 민주 시민으로서 참여할 수 있는 개인의 다짐 작성해보기 (100자 이상 입력)")
    user_input2 = st.text_area("여기에 입력합니다...", key="user_input2")
    st.caption(f"글자 수: {len(user_input2)}")

    if st.button("제출"):
        if not student_name.strip():
            st.error("성명을 입력합니다.")
        elif len(user_input1) >= 100 and len(user_input2) >= 100:
            try:
                with sqlite3.connect('user_inputs.db') as conn:
                    c = conn.cursor()
                    # 현재 날짜 및 시간 가져오기
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    chapter = "3.나의 생각"  # 현재 챕터 값 설정
                    # 질문 데이터를 딕셔너리로 구성
                    answers = {
                        "input1": user_input1,
                        "input2": user_input2
                    }

                    # JSON 형식으로 변환하여 저장
                    c.execute('''
                        INSERT INTO responses (student_id, student_name, chapter, answers, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (student_id, student_name, chapter, json.dumps(answers), timestamp))
                    conn.commit()
                st.success("입력한 의견과 학생 정보가 제출되었습니다.")
            except sqlite3.Error as e:
                st.error(f"데이터베이스 에러: {e}")
        else:
            st.error("각 의견을 최소 100자 이상 입력해야 제출할 수 있습니다.")

elif chapter == "교사 수업 관리":
    if st.session_state.is_admin:
        st.title("교사 수업 관리")

        with st.form("search_form"):
            search_student_id = st.number_input("학번으로 검색:", min_value=0, step=1, format="%d")
            search_student_name = st.text_input("이름으로 검색:")
            search_submit_button = st.form_submit_button("검색")
            show_all_button = st.form_submit_button("전체 데이터 보기")

        # 검색 결과 처리
        if search_submit_button:
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                query = """
                SELECT student_id, student_name, chapter, answers, timestamp 
                FROM responses 
                WHERE student_id LIKE ? AND student_name LIKE ?
                """
                # 검색 조건 적용
                c.execute(query, ('%' + str(search_student_id) + '%', '%' + search_student_name + '%'))
                data = c.fetchall()

        elif show_all_button:
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("SELECT student_id, student_name, chapter, answers, timestamp FROM responses")
                data = c.fetchall()
        else:
            data = None

        # 데이터를 DataFrame으로 변환
        if data:
            column_names = ["학번", "이름", "챕터", "의견1", "의견2", "의견3", "응답 시간"]
            df_data = []
            for row in data:
                student_id, student_name, chapter, answers_json, timestamp = row
                answers = json.loads(answers_json) if answers_json else {}
                df_data.append([
                    student_id, student_name, chapter, 
                    answers.get("input1", ""), 
                    answers.get("input2", ""), 
                    answers.get("input3", ""), 
                    timestamp
                ])

            if df_data:
                df = pd.DataFrame(df_data, columns=column_names)
                st.session_state.df = df  # 데이터를 세션 상태에 저장
                st.dataframe(df)  # 화면에 데이터 프레임 표시
            else:
                st.write("검색 결과가 없습니다.")

        # 엑셀 파일 생성 및 다운로드 버튼 처리
        if 'df' in st.session_state and not st.session_state.df.empty:
            if st.button("엑셀 파일 생성"):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl', datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
                    st.session_state.df.to_excel(writer, index=False, sheet_name='Responses')
                output.seek(0)
                st.session_state.output = output  # 생성된 파일을 세션 상태에 저장
                st.success("엑셀 파일이 생성되었습니다.")

            if 'output' in st.session_state:
                st.download_button(
                    label="엑셀 파일 다운로드",
                    data=st.session_state.output,
                    file_name="학생응답데이터.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.warning("로그인이 필요합니다.")