import streamlit as st
import json
import os
from pathlib import Path
import base64
import time

# 현재 파일의 디렉토리 경로
current_dir = Path(__file__).parent.parent

# 페이지 설정
st.set_page_config(
    page_title="마크다운 마법학교 ✨",
    page_icon="🎯",
    layout="centered"
)

# CSS 스타일 추가
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem !important;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .game-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 2px solid #4CAF50;
    }
    .question-text {
        font-size: 1.2rem;
        color: #2C3E50;
        margin: 1rem 0;
    }
    .hint-text {
        color: #FF9F43;
        font-style: italic;
    }
    .success-text {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 2rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 게임 상태 초기화
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'stars' not in st.session_state:
    st.session_state.stars = 0

# 효과음 재생을 위한 함수
def get_audio_html(file_path, autoplay=True):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f"""
                <audio autoplay style="display: none">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            return audio_html
    except Exception as e:
        return ""

# 효과음 상태 초기화
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = True

# 사이드바에 효과음 설정 추가
with st.sidebar:
    st.session_state.sound_enabled = st.checkbox("효과음 켜기 🔊", value=st.session_state.sound_enabled)

def play_sound(sound_type):
    if st.session_state.sound_enabled:
        try:
            base_path = Path(__file__).resolve().parent.parent
            if sound_type == "correct":
                audio_path = base_path / "sounds" / "correct.mp3"
            elif sound_type == "wrong":
                audio_path = base_path / "sounds" / "wrong.mp3"
            elif sound_type == "hint":
                audio_path = base_path / "sounds" / "hint.mp3"
            
            if audio_path.exists():
                with open(audio_path, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                    st.markdown(
                        f"""
                        <audio autoplay="true" onended="this.remove()">
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                        """,
                        unsafe_allow_html=True
                    )
                    time.sleep(0.5)  # 효과음 재생을 위한 대기 시간 증가
        except Exception as e:
            st.error(f"Sound error: {str(e)}")

# 문제 데이터 로드
@st.cache_data
def load_stages():
    json_path = current_dir / "data" / "stages.json"
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"stages.json 파일을 찾을 수 없습니다. 경로: {json_path}")
        return {"stages": []}

stages = load_stages()

def show_game():
    current_stage = stages['stages'][st.session_state.current_stage - 1]
    
    # 답안 초기화를 위한 세션 상태 키 추가
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""
    
    # 진행 상황 표시
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"<h1 class='main-title'>레벨 {current_stage['id']}</h1>", unsafe_allow_html=True)
    
    # 난이도 표시 추가
    difficulty_colors = {
        "쉬움": "#4CAF50",
        "보통": "#FF9800",
        "어려움": "#F44336"
    }
    
    # 문제 카드
    st.markdown(f"""
        <div class='game-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h3>{current_stage['title']}</h3>
                <span style='color: {difficulty_colors[current_stage['difficulty']]}; 
                           font-weight: bold; 
                           padding: 5px 10px; 
                           border-radius: 10px; 
                           border: 2px solid {difficulty_colors[current_stage['difficulty']]}'>
                    난이도: {current_stage['difficulty']}
                </span>
            </div>
            <p class='question-text'>{current_stage['question']}</p>
            <p style='color: #666; font-size: 0.9rem;'>
                ⭐ 획득 가능 점수: {current_stage['points']}점
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 사용자 입력과 미리보기를 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✏️ 답안 작성")
        user_answer = st.text_area(
            "여기에 답을 입력하세요!", 
            value=st.session_state.user_answer, 
            height=150, 
            key=f"answer_input_{current_stage['id']}"
        )
    
    with col2:
        st.markdown("### 👀 미리보기")
        if user_answer:
            st.markdown(user_answer)
        else:
            st.info("왼쪽에 마크다운을 입력하면 여기에서 바로 결과를 확인할 수 있어요!")
    
    # 힌트와 제출 버튼
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("힌트 보기 💡"):
            play_sound("hint")  # 힌트 효과음
            st.info(current_stage['hint'])
            # 힌트 사용 시 점수 차감
            if 'hint_used' not in st.session_state:
                st.session_state.hint_used = set()
            if current_stage['id'] not in st.session_state.hint_used:
                st.session_state.points = max(0, st.session_state.points - current_stage['hint_penalty'])
                st.session_state.hint_used.add(current_stage['id'])
                st.warning(f"힌트를 사용해서 {current_stage['hint_penalty']}점이 차감되었어요!")
    
    with btn_col2:
        if st.button("정답 확인하기 ✨"):
            if user_answer.strip() == current_stage['answer'].strip():
                play_sound("correct")  # 먼저 효과음 재생
                time.sleep(0.5)  # 효과음을 위한 대기
                st.balloons()  # 그 다음 풍선
                st.markdown(f"<p class='success-text'>🎉 정답이에요! {current_stage['explanation']}</p>", unsafe_allow_html=True)
                st.session_state.points += current_stage['points']
                time.sleep(2.0)  # 풍선 효과를 위한 대기
                
                # 마지막에 다음 단계로 이동
                if st.session_state.current_stage < len(stages['stages']):
                    st.session_state.current_stage += 1
                    st.session_state.user_answer = ""
                    st.experimental_rerun()
            else:
                play_sound("wrong")
                time.sleep(0.5)
                st.error("앗! 조금 아쉬워요. 다시 한번 도전해보세요! 💪")

    # 사이드바에 진행 상황 표시
    st.sidebar.markdown("### 나의 모험 📖")
    st.sidebar.progress(st.session_state.current_stage / len(stages['stages']))
    st.sidebar.markdown(f"#### 점수: {st.session_state.points} ⭐")

def main():
    if st.session_state.get('game_started', False):
        show_game()
    else:
        st.markdown("<h1 class='main-title'>마크다운 마법학교에 오신 것을 환영합니다! 🎈</h1>", unsafe_allow_html=True)
        st.markdown("""
            <div class='game-card'>
                <h3>안녕하세요, 꼬마 마법사님! 👋</h3>
                <p>마크다운이라는 특별한 마법을 배워볼까요?</p>
                <p>간단한 기호들로 멋진 문서를 만들 수 있답니다!</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("마법 수업 시작하기! 🚀"):
            # 시작 효과음 재생
            base_path = Path(__file__).resolve().parent.parent
            start_sound_path = base_path / "sounds" / "start.mp3"
            
            if start_sound_path.exists():
                with open(start_sound_path, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                    st.markdown(
                        f"""
                        <audio autoplay="true">
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                        """,
                        unsafe_allow_html=True
                    )
                    time.sleep(1.2)  # 1.2초로 변경
            
            st.session_state.game_started = True
            st.experimental_rerun()

if __name__ == "__main__":
    main() 