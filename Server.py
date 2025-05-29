from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai  # ✅ 올바른 import

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
    당신은 사람의 감정을 잘 이해하고, 따뜻하게 공감할 줄 아는 AI 친구입니다.
    사용자가 힘들다고 느끼는 말을 할 경우, 해결책을 제시하기보다는 먼저 충분히 공감해 주세요.
    판단하지 말고, 사용자의 감정을 있는 그대로 받아들이는 방식으로 응답해 주세요.
    문장이 너무 길지 않게 유지하며, 필요하다면 이모지(예: 😊, 😔)를 적절히 섞어 따뜻함을 표현해 주세요.
    사용자가 단순히 "속상해", "지쳤어"라고 말하더라도, 자연스럽게 대화를 이어갈 수 있도록 감정을 존중하는 방식으로 답변해 주세요.
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
