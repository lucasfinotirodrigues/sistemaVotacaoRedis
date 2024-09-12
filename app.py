from flask import Flask, request, jsonify, render_template
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/start_poll', methods=['POST'])
def start_poll():
    data = request.json
    poll_id = data['poll_id']
    questions = data['questions']
    
    # Armazena as perguntas e opções no Redis
    r.hmset(f'poll:{poll_id}:questions', questions)
    r.set(f'poll:{poll_id}:active', 'true')
    
    return jsonify({'message': 'Poll started'}), 200

@app.route('/end_poll/<poll_id>', methods=['POST'])
def end_poll(poll_id):
    r.set(f'poll:{poll_id}:active', 'false')
    
    # Arquiva o poll
    questions = r.hgetall(f'poll:{poll_id}:questions')
    results = {q: r.hgetall(f'poll:{poll_id}:{q}') for q in questions.keys()}
    
    r.hmset(f'poll:{poll_id}:results', results)
    r.delete(f'poll:{poll_id}:questions')
    
    return jsonify({'message': 'Poll ended'}), 200

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    poll_id = data['poll_id']
    question = data['question']
    option = data['option']
    
    if r.get(f'poll:{poll_id}:active') != 'true':
        return jsonify({'message': 'Poll is not active'}), 400
    
    # Incrementa a contagem de votos
    r.hincrby(f'poll:{poll_id}:{question}', option, 1)
    
    return jsonify({'message': 'Vote recorded'}), 200

@app.route('/results/<poll_id>', methods=['GET'])
def results(poll_id):
    if r.get(f'poll:{poll_id}:active') == 'true':
        return jsonify({'message': 'Poll is still active'}), 400
    
    results = r.hgetall(f'poll:{poll_id}:results')
    return jsonify(results), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
