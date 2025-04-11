from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

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