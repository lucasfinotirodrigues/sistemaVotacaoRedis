import redis
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/start_poll', methods=['POST'])
def start_poll():
    data = request.json
    poll_id = data['poll_id']
    questions = data['questions']
    
    # Converter perguntas e opções para JSON
    questions_json = json.dumps(questions)
    
    # Armazenar no Redis
    r.set(f"poll:{poll_id}:questions", questions_json)
    
    return jsonify(message="Poll started")

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    poll_id = data['poll_id']
    question = data['question']
    option = data['option']
    
    # Construir a chave para a votação
    key = f"poll:{poll_id}:votes:{question}:{option}"
    
    # Incrementar o contador de votos
    r.incr(key)
    
    return jsonify(message="Vote recorded")

@app.route('/results/<poll_id>', methods=['GET'])
def results(poll_id):
    keys = r.keys(f"poll:{poll_id}:votes:*")
    results = {key: int(r.get(key)) for key in keys}
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
