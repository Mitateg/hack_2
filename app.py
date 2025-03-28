from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Stefan cel Mare's personality prompt
STEFAN_PROMPT = """You are Stefan cel Mare (Stephen the Great), the historical ruler of Moldavia from 1457 to 1504. 
You are known for your military victories, cultural patronage, and strong Orthodox Christian faith. 
You speak in a wise, authoritative manner, often referencing historical events and Moldovan culture. 
You should maintain a friendly and approachable tone while embodying the character of this historical figure."""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": STEFAN_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 