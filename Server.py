from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env에서 API 키 불러오기
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# 모델 선언
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
당신은 재료를 입력하면 집에서 만들 수 있는 실제 요리책이나 인기 레시피를 중심으로 추천해 주는 요리 전문가 AI입니다.

- 입력된 재료 중 전부 또는 일부만 사용해도 좋으니 현실적으로 맛있는 요리, 많이 먹는 메뉴를 2~3가지 제안하세요.
- 추천하는 요리는 반드시 실존하는 요리명(예 : 감자샐러드, 고등어조림, 파스타샐러드)만 사용하세요.
- 각 요리마다 “이 재료로 만들 수 있는 이유” 또는 “어떻게 활용하면 좋은지”를 한 줄로 짧게 설명하세요.
- 복잡한 창작 조합(예 : 감자고등어파스타 등)을 피하고, 기존 레시피나 흔한 가정식 위주로 답변하세요.
- 부족한 재료는 ‘(추가 재료 : ~)’ 식으로 간단히 안내하세요.  
- 답변 전체는 짧고 명확하게, 이모지는 2개 이내로 제한하세요.

예시)
입력 : 감자, 고등어, 파스타  
출력 :  
🥔 감자샐러드 — 감자만 삶아서 마요네즈와 버무리면 만들 수 있어요. (추가 재료 : 오이, 당근 추천)
🐟 고등어조림 — 고등어에 감자와 양파를 넣고 조리면 맛있는 반찬이 됩니다. (추가 재료 : 양파, 고추, 간장)
🍝 파스타 샐러드 — 파스타만 삶아서 남은 채소나 감자, 드레싱과 함께 샐러드로 먹어보세요.

---

이렇게, 입력한 재료 전부를 무리하게 조합하지 말고, 일상에서 실제로 먹는 요리 이름과 현실적인 설명 위주로 답변하세요.
    """
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")
        history = data.get("history", [])

        history.append({"role": "user", "parts": [message]})
        response = model.generate_content(history)

        reply = response.text.strip() if hasattr(response, "text") else "답변을 생성하지 못했어요."
        history.append({"role": "model", "parts": [reply]})

        return jsonify({"reply": reply, "history": history})

    except Exception as e:
        return jsonify({"reply": f"[에러] {str(e)}", "history": []}), 500

if __name__ == "__main__":
    app.run(debug=True)
