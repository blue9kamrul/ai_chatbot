from flask import Flask, render_template, request, jsonify
import openai, os, csv
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()


app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load FAQs
faq_list = []
with open('data/faqs.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    faq_list = list(reader)

def check_faq(user_input):
    for faq in faq_list:
        if faq['question'].lower() in user_input.lower():
            return faq['answer']
    return None

def get_bot_response(user_input):
    # 1. Try to answer from FAQ
    faq_answer = check_faq(user_input)
    if faq_answer:
        return faq_answer

    # 2. Fall back to AI for everything else
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a business."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error talking to OpenAI: {e}"



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_message = get_bot_response(user_message)
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    app.run(debug=True)
