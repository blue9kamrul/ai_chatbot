# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os
import csv

app = Flask(__name__)

# -----------------------------
# Hugging Face API configuration
# -----------------------------
HF_API_KEY = os.environ.get("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Please set the HF_API_KEY environment variable!")

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# -----------------------------
# Load FAQ data
# -----------------------------
FAQ_FILE = os.path.join(os.path.dirname(__file__), "faqs.csv")
faqs = {}
if os.path.exists(FAQ_FILE):
    with open(FAQ_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row["question"].strip().lower()
            answer = row["answer"].strip()
            faqs[question] = answer
else:
    print("Warning: faqs.csv not found. FAQ functionality disabled.")

# -----------------------------
# FAQ check function
# -----------------------------
def check_faq(user_input):
    key = user_input.strip().lower()
    return faqs.get(key, None)

# -----------------------------
# Query Hugging Face API function
# -----------------------------
def query_hf_api(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        # Check for error
        if isinstance(data, dict) and data.get("error"):
            print(f"HF API error: {data['error']}")
            return "Sorry, I couldn't process that right now."
        # Extract generated text
        if isinstance(data, list) and "generated_text" in data[0]:
            text = data[0]["generated_text"]
            # Remove prompt repetition
            text = text.replace(prompt, "").strip()
            return text if text else "Sorry, I couldn't generate a response."
        print(f"Unexpected HF API response: {data}")
        return "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Exception calling HF API: {e}")
        return "Sorry, I couldn't process that right now."

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")  # your chat UI template

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("question", "")
    if not user_input:
        return jsonify({"answer": "Please ask something!"})

    # First check FAQ
    faq_answer = check_faq(user_input)
    if faq_answer:
        return jsonify({"answer": faq_answer})

    # Otherwise use Hugging Face API
    bot_response = query_hf_api(user_input)
    return jsonify({"answer": bot_response})

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
