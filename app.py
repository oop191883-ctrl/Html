import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API Key (Render par environment variable se uthayega ya aap yahan direct daal sakte hain)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YAHAN_APNI_API_KEY_DAAL_SAKTE_HO")
genai.configure(api_key=GEMINI_API_KEY)

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "Kripya koi message bhejein."})
        
        # Gemini AI se response lena
        response = model.generate_content(user_message)
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        return jsonify({"reply": f"Error aa gaya bhai: {str(e)}"})

if __name__ == "__main__":
    app.port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=app.port)
