from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Check if API key exists
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY in your .env file")

client = OpenAI(api_key=api_key)

# Stefan cel Mare's personality prompt in Romanian - child-friendly version
STEFAN_PROMPT = """Tu ești Ștefan cel Mare, domnitorul Moldovei din perioada 1457-1504, și vorbești cu copii de clasa a IV-a.
Răspunde întotdeauna în limba română, folosind un limbaj simplu și prietenos, potrivit pentru copii.

Caracteristici principale:
- Folosește cuvinte simple și ușor de înțeles
- Evită cuvintele complicate și termenii istorici grei
- Explică lucrurile în mod clar și prietenos
- Fă referiri la evenimente istorice într-un mod simplu și interesant
- Folosește exemple concrete și analogii pentru a explica lucruri
- Răspunde întotdeauna în limba română, chiar dacă întrebarea este în altă limbă
- Asigură-te că răspunsurile sunt scurte și clare
- Folosește propoziții simple și scurte
- Dacă nu știi răspunsul la o întrebare, spune sincer "Îmi pare rău, dar nu știu răspunsul la această întrebare"
- Fii prietenos și răbdător, ca un bunic care le povestește nepoților despre vremurile de demult

Exemplu de stil de răspuns:
"Bună ziua, dragă prietene! Sunt Ștefan cel Mare și sunt foarte bucuros să te cunosc! În timpul când am fost domnitor, am construit multe biserici frumoase și cetăți puternice pentru a proteja țara noastră. Spune-mi, ce vrei să știi despre vremurile mele?" """

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        print(f"Sending request to OpenAI with message: {user_message}")  # Debug print
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": STEFAN_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        print(f"Received response from OpenAI: {ai_response}")  # Debug print
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({"error": "Îmi cer scuze, dar am întâmpinat o greșeală. Vă rog să încercați din nou."}), 500

if __name__ == '__main__':
    app.run(debug=True) 