import streamlit as st
import requests

# OpenAI API 키 설정
api_key = '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'
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 질문을 저장할 리스트
questions_list = []

def get_response(question):
    """OpenAI API를 사용하여 주어진 질문에 대한 답변을 가져오는 함수"""
    prompt = f"주 {question}에 대해 상세한 공부 일정을 계획하고 각 과목별 정확한 시간을 명시하며, 단순한 상식이 아닌 실제로 도움이 되는 2-3가지 공부 팁을 제공해주세요."
    data = {
        "model": "gpt-3.5-turbo-0125",  # GPT-4 모델 선택
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"


# 스트림릿 애플리케이션 구성
def main():
    st.title("지식 아케이드")  # 타이틀 변경

    study_schedule = {}
    selected_days = st.multiselect("공부를 원하는 요일을 선택하세요:", ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"])
    for day in ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]:
        if day in selected_days:
            subjects_options = ["영어", "수학", "과학", "역사", "국어", "기타"]
            for subject in subjects_options:
                key = f"{day}_{subject}"  # 각 슬라이더에 대해 고유한 key 생성
                if subject == "기타":
                    custom_subject = st.text_input(f"기타 과목을 입력하세요 ({day}):")
                    if custom_subject:
                        study_hours = st.slider(f"{custom_subject} 공부 시간을 선택하세요 (시간)", 0, 12, value=0, key=key)
                        study_schedule.setdefault(day, {}).setdefault(custom_subject, study_hours)
                else:
                    study_hours = st.slider(f"{subject} 공부 시간을 선택하세요 (시간)", 0, 12, value=0, key=key)
                    study_schedule.setdefault(day, {}).setdefault(subject, study_hours)

    # 질문이 입력되면 답변 받기
    if st.button("질문하기"):
        for day, subjects in study_schedule.items():
            if subjects:
                selected_subjects_str = ', '.join(subjects)
                question = f"{day} / {selected_subjects_str}"
                answer = get_response(question)

                # 최종 답변 출력
                st.subheader("최고의 답변입니다:")
                st.write(answer)

                # 질문을 리스트에 추가
                questions_list.append(question)

    # 사이드바에 모든 질문 출력
    st.sidebar.title("이전 질문")
    for question in questions_list:
        st.sidebar.write(question)

if __name__ == "__main__":
    main()