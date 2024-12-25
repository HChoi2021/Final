import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="기후 변화와 나의 생활", layout="wide")

# 세션 상태 초기화 및 유지
if 'user_input1' not in st.session_state:
    st.session_state.user_input1 = ""
if 'user_input2' not in st.session_state:
    st.session_state.user_input2 = ""

# 수업 차시 선택을 위한 사이드바
chapter = st.sidebar.radio(
    "수업 순서",
    ("들어가며", "1차시 기본 개념 이해", "2차시 그래프 시각화 도구로 지구 온난화 이해하기", "3차시 나의 생각")
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

elif chapter == "2차시 그래프 시각화 도구로 지구 온난화 이해하기":
    st.header("2차시 그래프 시각화 도구로 지구 온난화 이해하기")
    st.write("""
        다양한 그래프 시각화 도구를 사용하여 지구 온난화의 영향을 살펴봅니다.
        예를 들어, 지난 100년 동안의 온도 변화 그래프를 분석합니다.
    """)

elif chapter == "3차시 나의 생각":
    st.header("3차시 나의 생각")
    st.write("앞에서 배운 내용에 대해 여러분의 생각을 정리해보는 공간입니다.")

    # 입력 1
    st.subheader("1) 지구 온난화를 해결할 수 있는 방법 제안해보기:")
    user_input1_temp = st.text_area("여기에 입력해주세요...", key="user_input1_temp")
    st.write(f"글자 수: {len(user_input1_temp)}")

    if st.button("제출1", key="submit1"):
        if len(user_input1_temp) >= 100:  # 최소 글자 수 검사
            st.session_state.user_input1 = user_input1_temp
            st.success("입력하신 의견이 제출되었습니다.")
            st.write("입력하신 의견:", st.session_state.user_input1)
        else:
            st.error("최소 100자 이상 입력해야 제출할 수 있습니다.")  # 글자 수 부족 경고

    st.write("")  # 의견 1과 의견 2 사이 공간 추가

    # 입력 2
    st.subheader("2) 민주 시민으로서 참여할 수 있는 개인의 다짐 작성해보기:")
    user_input2_temp = st.text_area("여기에 입력해주세요...", key="user_input2_temp")
    st.write(f"글자 수: {len(user_input2_temp)}")

    if st.button("제출2", key="submit2"):
        if len(user_input2_temp) >= 100:  # 최소 글자 수 검사
            st.session_state.user_input2 = user_input2_temp
            st.success("입력하신 의견이 제출되었습니다.")
            st.write("입력하신 의견:", st.session_state.user_input2)
        else:
            st.error("최소 100자 이상 입력해야 제출할 수 있습니다.")  # 글자 수 부족 경고