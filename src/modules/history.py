import os
import streamlit as st
from streamlit_chat import message

class ChatHistory:
    
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def default_greeting(self):
        return "안녕! Save Mate! 👋"

    def default_prompt(self, topic):
        return f"""사이드바에서 유저아이디/금융상품종류를 입력해주세요. 입력하지 않으면 게스트모드/일반채팅모드로 실행이 됩니다.

        정확한 정보를 안내해 드리기 위해 열심히 학습하고 있지만, 가끔은 실수를 할 수도 있습니다. 
        현재 상담 시점에서 충족하시는 조건을 고려해 상품을 안내드리고 있어요. 저와 상담하신 후에 충족되는 조건은 고려할 수 없습니다. 

        가이드라인을 참고하세요.
        [마이데이터 기반 예금/적금상품 추천 기능]
        1. 유저아이디를 사이드바에서 입력하세요. 
        2. 채팅창에 내 계좌정보 알려줘를 입력해주세요.
        3. 이후, 원하시는 조건 + 추천해줘를 입력해주세요.
        4. 원하시는 조건의 예시로는 군인, 청춘, 20대, 50대가 있습니다.
        5. 마이데이터에서 계좌잔액, 주거래은행 등의 정보를 반영해서 예금자보호법에 따라 상품을 추천합니다.

        [상품정보 검색 기능]
        1. 채팅창에 원하시는 상품명 + 궁금한 내용을 입력하세요.
        2. 현재 10여개 은행의 50여개의 상품정보가 준비되어 있습니다.
        3. 상품명 예시: 우리 SUPER주거래 정기적금, 급여하나 월복리 적금, 행복knowhow 연금예금, NH장병내일준비적금

        [금융정보 기능]
        1. 궁금하신 금융정보를 채팅창에 자유롭게 물어보세요.
        2. 금융정보 예시: 복리, 예금자보호법, 인플레이션

        
        질문 예시
        당신의 금융 목표와 선호도에 대해 더 자세히 알려주시면 더 정확한 상품 추천을 드릴 수 있습니다. 
        1. 어떤 금융 목표를 달성하고 싶으신가요? (예: 목돈 모으기, 주택 구매, 여행 자금 등) 
        2. 예금 또는 적금에 얼마나 많은 금액을 투자하고 싶으신가요? 
        3. 예금 또는 적금의 기간은 어느 정도로 생각하고 계신가요? (예: 단기, 중기, 장기) 
        4. 우대금리를 받기 위해 어떤 조건을 충족하실 수 있으신가요? (예: 급여 이체, 카드 이용, 마케팅 동의 등)
 
        고객님, 어떤게 궁금하신가요? 🤗 """

    def initialize_user_history(self):
        st.session_state["user"] = [self.default_greeting()]

    def initialize_assistant_history(self, uploaded_file):
        # uploaded_file 안쓰도록
        st.session_state["assistant"] = [self.default_prompt(uploaded_file)] #[self.default_prompt(uploaded_file.name)]

    def initialize(self, uploaded_file):
        if "assistant" not in st.session_state:
            print('assistant session state')
            self.initialize_assistant_history(uploaded_file)
        if "user" not in st.session_state:
            print('user session state')
            self.initialize_user_history()

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        
        self.initialize_user_history()
        self.initialize_assistant_history(uploaded_file)
        st.session_state["reset_chat"] = False

    def append(self, mode, message):
        print('history append method')
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    message(
                        st.session_state["user"][i],
                        is_user=True,
                        key=f"history_{i}_user",
                        avatar_style="big-smile",
                    )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="identicon")

    def load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()

    def save(self):
        with open(self.history_file, "w") as f:
            f.write("\n".join(self.history))
