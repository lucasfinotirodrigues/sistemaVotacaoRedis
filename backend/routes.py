from flask import request, jsonify
from app import app
from models import iniciar_votacao, registrar_voto, obter_resultados, encerrar_votacao

@app.route('/iniciar_votacao', methods=['POST'])
def iniciar_votacao_route():
    dados = request.json
    sessao_id = dados.get('sessao_id')
    perguntas = dados.get('perguntas')
    iniciar_votacao(sessao_id, perguntas)
    return jsonify({"status": "Votação iniciada"}), 200

@app.route('/votar', methods=['POST'])
def votar_route():
    dados = request.json
    sessao_id = dados.get('sessao_id')
    pergunta = dados.get('pergunta')
    opcao = dados.get('opcao')
    registrar_voto(sessao_id, pergunta, opcao)
    return jsonify({"status": "Voto registrado"}), 200

@app.route('/resultados/<sessao_id>', methods=['GET'])
def resultados_route(sessao_id):
    resultados = obter_resultados(sessao_id)
    return jsonify(resultados), 200

@app.route('/encerrar_votacao/<sessao_id>', methods=['POST'])
def encerrar_votacao_route(sessao_id):
    resultados = encerrar_votacao(sessao_id)
    return jsonify(resultados), 200

if __name__ == '__main__':
    app.run(debug=True)
