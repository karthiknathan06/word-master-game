from flask import Flask, jsonify, request, render_template, send_from_directory
import random
from gtts import gTTS
import os
import requests

app = Flask(__name__)

api_data = []

def initialize():
    global api_data
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    api_data = response.content.splitlines()

def getMeaning(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data=response.json()
        if 'meanings' in data[0]:
            definitions = []
            for meaning in data[0]['meanings']:
                if 'definitions' in meaning:
                    definition=meaning['definitions'][0]
                    definition=definition['definition']
                    print(definition)
        else:
            definitions = "None"
        return "Meaning: "+definition
    else:
        return "None"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word', methods=['GET'])
def get_word():
    global api_data
    if(api_data==[]):
        initialize()
    word = random.choice(api_data)
    decoded_word=word.decode()
    tts = gTTS(text=decoded_word, lang='en')
    tts.save("static/output.mp3")
    meaning_response = getMeaning(decoded_word)
    return jsonify(word=decoded_word, meaning=meaning_response)

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory('static', filename)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    answer = data['answer']
    word = data['word']
    result = (answer.lower() == word.lower())
    return jsonify(correct=result)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
