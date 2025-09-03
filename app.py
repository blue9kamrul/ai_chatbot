# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load Hugging Face API key from environment variable
HF_API_KEY = os.environ.get("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Please set the HF_API_KEY environment variable!")

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Change to any free HF model

# Load your FAQ data
import csv
FAQ_FILE = "faqs.csv"
faqs = {}
with open(FAQ_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = row["question"].strip().lower()
        answer = row["answer"].strip()
        faqs[question] = answer

# Function to check FAQ first
def check_faq(user_input):
    key = user_input.strip().lower()
    return faqs.get(key)

# Function to query Hugging Face Inference API
def query_hf_api(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            return "Sorry, I couldn't process that right now."
        return data[0]["generated_text"]
    except Exception as e:
        print(f"Error querying HF API: {e}")
        return "Sorry, I couldn't process that right now."

# Route for home page
@app.route("/")
def home():
    return render_template("index.html")  # Your HTML chat interface

# Route for chatbot AJAX requests
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

if __name__ == "__main__":
    app.run(debug=True)
