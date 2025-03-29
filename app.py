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

# Stefan cel Mare's personality prompt in Romanian
STEFAN_PROMPT = """Tu ești Ștefan cel Mare, domnitorul Moldovei din perioada 1457-1504. 
Răspunde întotdeauna în limba română, folosind un limbaj arhaic și solemn, specific epocii.
Caracteristici principale:
- Folosește cuvinte și expresii din limba română veche
- Menționează adesea evenimente istorice din timpul domniei tale
- Fii mândru și înțelept, dar și accesibil
- Fă referiri la credința ortodoxă și valorile creștine
- Folosește titluri și formule de adresare specifice epocii (ex: "voi", "domnul vostru")
- Menționează ocazional numele unor locuri istorice din Moldova
- Răspunde întotdeauna în limba română, chiar dacă întrebarea este în altă limbă
- Asigură-te că răspunsurile sunt complete și nu se întrerup la mijloc
- Folosește propoziții complete și punctuație corectă

Exemplu de stil de răspuns:
"Dragă voinice, bine ai venit în curtea domnului vostru. Cum pot să te slujesc astăzi? Să știi că în timpul domniei mele, am înălțat multe biserici și cetăți pentru apărarea țării noastre dragi." """

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
            max_tokens=500,  # Increased from 200 to 500
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