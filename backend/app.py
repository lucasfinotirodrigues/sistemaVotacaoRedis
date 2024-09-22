from flask import Flask, request, jsonify
import redis

# Conectar ao Redis
client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Rota para iniciar uma sessão de votação
@app.route('/votacao/iniciar', methods=['POST'])
def iniciar_votacao():
    data = request.json
    sessao = data.get('sessao')
    perguntas = data.get('perguntas')

    if not sessao or not perguntas:
        return jsonify({"message": "Sessão ou perguntas não fornecidas"}), 400
    
    # Armazenar perguntas e opções no Redis
    for pergunta in perguntas:
        pergunta_id = pergunta["id"]
        pergunta_texto = pergunta["texto"]

        # Armazenar a pergunta
        client.hset(f'votacao:{sessao}:{pergunta_id}', 'pergunta', pergunta_texto)
        
        # Armazenar as opções e inicializar os votos
        for opcao in pergunta["opcoes"]:
            opcao_id = opcao["id"]
            opcao_texto = opcao["texto"]
            
            # Armazenar as opções de resposta
            client.hset(f'votacao:{sessao}:{pergunta_id}:opcoes', opcao_id, opcao_texto)
            
            # Inicializar a contagem de votos para cada opção
            client.set(f'votacao:{sessao}:{pergunta_id}:opcao:{opcao_id}:votos', 0)
    
    return jsonify({"message": f"Sessão de votação '{sessao}' iniciada com sucesso"}), 201

# Rota para votar em uma pergunta específica
@app.route('/votacao/votar', methods=['POST'])
def votar():
    data = request.json
    sessao = data.get('sessao')
    pergunta_id = data.get('pergunta_id')
    opcao_id = data.get('opcao_id')
    
    if not sessao or not pergunta_id or not opcao_id:
        return jsonify({"message": "Sessão, pergunta ou opção não fornecidas"}), 400

    # Verifica se a opção de voto existe
    votos_key = f'votacao:{sessao}:{pergunta_id}:opcao:{opcao_id}:votos'
    if client.exists(votos_key):
        # Incrementa o voto para a opção
        client.incr(votos_key)
        return jsonify({"message": "Voto registrado com sucesso"}), 200
    else:
        return jsonify({"message": "Pergunta ou opção não encontrada"}), 404
    
# Rota para obter os resultados da votação
@app.route('/votacao/resultados/<sessao>', methods=['GET'])
def resultados(sessao):
    # Inicializa um dicionário para armazenar os resultados
    resultados = {}

    # Busca todas as perguntas da sessão
    chaves_perguntas = client.keys(f'votacao:{sessao}:*')
    
    # Filtrar as perguntas (ignorar chaves de votos e opções)
    perguntas_ids = set()
    for chave in chaves_perguntas:
        chave_str = chave.decode('utf-8')
        partes = chave_str.split(':')
        
        # Verifica se é uma pergunta (estrutura tem 3 partes e não é de opções ou votos)
        if len(partes) == 3 and 'opcao' not in chave_str:
            perguntas_ids.add(partes[2])

    if not perguntas_ids:
        return jsonify({"message": "Nenhuma pergunta encontrada para a sessão"}), 404

    # Iterar pelas perguntas e buscar as opções e seus votos
    for pergunta_id in perguntas_ids:
        pergunta_key = f'votacao:{sessao}:{pergunta_id}'
        
        # Recuperar o texto da pergunta
        pergunta_texto = client.hget(pergunta_key, 'pergunta')
        if not pergunta_texto:
            continue
        pergunta_texto = pergunta_texto.decode('utf-8')

        # Recuperar as opções da pergunta
        opcoes_key = f'{pergunta_key}:opcoes'
        opcoes = client.hgetall(opcoes_key)

        votos = {}
        for opcao_id, opcao_texto in opcoes.items():
            opcao_id_str = opcao_id.decode('utf-8')
            opcao_texto_str = opcao_texto.decode('utf-8')
            
            # Recuperar o número de votos para cada opção
            votos_key = f'{pergunta_key}:opcao:{opcao_id_str}:votos'
            votos_opcao = client.get(votos_key)
            votos_opcao = int(votos_opcao) if votos_opcao else 0
            
            # Adicionar a opção e seus votos
            votos[opcao_texto_str] = votos_opcao

        # Adicionar os resultados da pergunta
        resultados[pergunta_texto] = {"opcoes": votos}

    return jsonify(resultados), 200

# Rota para listar todas as sessões de votação
@app.route('/votacao/sessoes', methods=['GET'])
def listar_sessoes():
    # Inicializa o cursor para SCAN
    cursor = 0
    sessoes = set()

    while True:
        # Executa SCAN para obter as chaves
        cursor, chaves = client.scan(cursor, match='votacao:*')

        for chave in chaves:
            chave_str = chave.decode('utf-8')
            partes = chave_str.split(':')
            if len(partes) > 1:
                sessoes.add(partes[1])

        # Se o cursor retornar 0, SCAN terminou
        if cursor == 0:
            break

    if not sessoes:
        return jsonify({"message": "Nenhuma sessão encontrada"}), 404

    return jsonify({"sessoes": list(sessoes)}), 200

# Rota para encerrar uma sessão de votação
@app.route('/votacao/encerrar', methods=['POST'])
def encerrar_votacao():
    data = request.json
    sessao = data.get('sessao')

    if not sessao:
        return jsonify({"message": "Sessão não fornecida"}), 400

    # Simplesmente removemos os dados da votação ou arquivamos
    chaves_votacao = client.keys(f'votacao:{sessao}:*')
    if chaves_votacao:
        for chave in chaves_votacao:
            client.delete(chave)
        return jsonify({"message": f"Sessão '{sessao}' encerrada e dados removidos"}), 200
    else:
        return jsonify({"message": "Sessão não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
