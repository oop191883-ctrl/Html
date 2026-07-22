import os
from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)

API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an expert AI programming assistant. Write clean code blocks."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {{API_KEY}}",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {{str(e)}}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
