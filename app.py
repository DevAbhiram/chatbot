from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=""
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:5000",  # Replace with your site URL if hosted
                "X-Title": "Local Chatbot"
            },
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[
    {"role": "user", "content": f"{user_input}. Respond directly without extra explanation."}]

        )

        reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Error processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
