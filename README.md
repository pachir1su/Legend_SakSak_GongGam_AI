# ㄹㅈㄷ 싹싹 공감 AI 

Gemini API를 활용하여 만든 공감형 챗봇. 

- Gemini API를 이용해 만든 웹사이트 기본 형식
- React로 만들면 좋을듯
- Gemini 프롬포트를 공감 AI에 맞게 수정.

---

## ✨ 주요 기능

- 🤖 Google Gemini API 기반 공감형 대화
- 🌗 라이트/다크 모드 전환 버튼
- 💬 실시간 채팅 인터페이스
- 🕓 시간 스탬프 표시
- 🔄 Gemini 입력 중 애니메이션 표시

---

## 🔧 설치 및 실행

### 1. 환경 설정
```bash
git clone https://github.com/pachir1su/Legend_SakSak_GongGam_AI.git
cd Legend_SakSak_GongGam_AI
python -m venv venv
venv\Scripts\activate  # (Windows 기준)
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성 후 아래와 같이 작성:

```
GOOGLE_API_KEY=YOUR_API_KEY
```

### 3. 실행
```bash
python server.py
```

웹 브라우저에서 `http://127.0.0.1:5000` 접속

---

## 🗂️ 프로젝트 구조

```
📁 static/
    ├── main.js
    └── style.css
📁 templates/
    └── index.html
.env
server.py
README.md
```

---
