document.getElementById('toggleVotacao').addEventListener('click', function() {
    const sections = document.querySelectorAll('.votacao-iniciar, .votar, .resultados, .hidden');
    sections.forEach(section => {
        section.classList.toggle('hidden');
    });
});

document.getElementById('iniciarVotacaoForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  
  const sessao = document.getElementById('sessao').value;
  const perguntas = JSON.parse(document.getElementById('perguntas').value);

  try {
      const response = await fetch('/votacao/iniciar', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ sessao, perguntas }),
      });

      const data = await response.json();
      document.getElementById('iniciarVotacaoMessage').innerText = data.message;
  } catch (error) {
      console.error('Erro ao iniciar votação:', error);
  }
});

document.getElementById('votarForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const sessao = document.getElementById('sessaoVotar').value;
  const pergunta_id = document.getElementById('perguntaId').value;
  const opcao_id = document.getElementById('opcaoId').value;

  try {
      const response = await fetch('/votacao/votar', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ sessao, pergunta_id, opcao_id }),
      });

      const data = await response.json();
      document.getElementById('votarMessage').innerText = data.message;
  } catch (error) {
      console.error('Erro ao votar:', error);
  }
});

document.getElementById('resultadosForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const sessao = document.getElementById('sessaoResultados').value;

  try {
      const response = await fetch(`/votacao/resultados/${sessao}`);
      const data = await response.json();
      document.getElementById('resultadosDisplay').innerText = JSON.stringify(data, null, 2);
  } catch (error) {
      console.error('Erro ao obter resultados:', error);
  }
});




document.addEventListener("DOMContentLoaded", function () {
  const listaSessoes = document.getElementById("sessoes-lista");

  async function carregarSessoes() {
      try {
          const response = await fetch("http://127.0.0.1:5000/votacao/sessoes");
          if (!response.ok) {
              if (response.status === 404) {
                  listaSessoes.innerHTML = "<li>Nenhuma sessão encontrada</li>";
              }
              throw new Error(`Erro ao carregar as sessões: ${response.statusText}`);
          }

          const data = await response.json();

          if (data.sessoes && Object.keys(data.sessoes).length > 0) {
              listaSessoes.innerHTML = ""; // Limpa a lista antes de adicionar os itens

              Object.keys(data.sessoes).forEach(sessaoId => {
                  const sessaoLi = document.createElement("li");
                  sessaoLi.textContent = `Sessão: ${sessaoId}`;
                  const ulPerguntas = document.createElement("ul");

                  Object.keys(data.sessoes[sessaoId].perguntas).forEach(perguntaId => {
                      const pergunta = data.sessoes[sessaoId].perguntas[perguntaId];
                      const perguntaLi = document.createElement("li");
                      perguntaLi.textContent = `Pergunta: ${pergunta.id} - ${pergunta.texto}`; // Exibe o ID e texto da pergunta
                      const ulOpcoes = document.createElement("ul");

                      pergunta.opcoes.forEach(opcao => {
                          const opcaoLi = document.createElement("li");
                          opcaoLi.textContent = `Opção: ${opcao.id} - ${opcao.texto}`; // Exibe o ID e texto da opção
                          ulOpcoes.appendChild(opcaoLi);
                      });

                      perguntaLi.appendChild(ulOpcoes); // Adiciona a lista de opções à pergunta
                      ulPerguntas.appendChild(perguntaLi); // Adiciona a pergunta à lista de perguntas
                  });

                  sessaoLi.appendChild(ulPerguntas); // Adiciona a lista de perguntas à sessão
                  listaSessoes.appendChild(sessaoLi); // Adiciona a sessão à lista de sessões
              });
          } else {
              listaSessoes.innerHTML = "<li>Nenhuma sessão encontrada</li>";
          }
      } catch (error) {
          console.error("Erro ao carregar as sessões:", error);
          listaSessoes.innerHTML = "<li>Erro ao carregar as sessões</li>";
      }
  }

  carregarSessoes();
});



document.getElementById('encerrarVotacaoForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const sessao = document.getElementById('sessaoEncerrar').value;

  try {
      const response = await fetch('/votacao/encerrar', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ sessao }),
      });

      const data = await response.json();
      document.getElementById('encerrarVotacaoMessage').innerText = data.message;

      // Opcional: atualizar a lista de sessões após a exclusão
  } catch (error) {
      console.error('Erro ao encerrar sessão:', error);
      document.getElementById('encerrarVotacaoMessage').innerText = 'Erro ao encerrar sessão.';
  }
});


