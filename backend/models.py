# models.py

def iniciar_votacao(sessao_id, perguntas):
    """
    Inicia uma sessão de votação armazenando perguntas e opções de resposta no Redis.
    """
    r.hmset(f"votacao:{sessao_id}:perguntas", perguntas)
    for pergunta, opcoes in perguntas.items():
        for opcao in opcoes:
            r.set(f"votacao:{sessao_id}:votos:{pergunta}:{opcao}", 0)

def registrar_voto(sessao_id, pergunta, opcao):
    """
    Incrementa a contagem de votos para uma opção específica.
    """
    r.incr(f"votacao:{sessao_id}:votos:{pergunta}:{opcao}")

def obter_resultados(sessao_id):
    """
    Obtém os resultados da votação para cada pergunta e opção.
    """
    resultados = {}
    perguntas = r.hgetall(f"votacao:{sessao_id}:perguntas")
    for pergunta in perguntas:
        resultados[pergunta] = {}
        opcoes = perguntas[pergunta]
        for opcao in opcoes:
            contagem = r.get(f"votacao:{sessao_id}:votos:{pergunta}:{opcao}")
            resultados[pergunta][opcao] = int(contagem)
    return resultados

def encerrar_votacao(sessao_id):
    """
    Arquiva os resultados e encerra a votação.
    """
    resultados = obter_resultados(sessao_id)
    # Aqui você pode salvar os resultados em um banco de dados ou exportar para um arquivo
    return resultados
