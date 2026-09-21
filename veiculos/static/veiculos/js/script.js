function carregarVeiculos() {
    // Faz a chamada para a rota unificada que criamos no Django
    fetch('/api/estacionamento/dados/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar dados do servidor.');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'sucesso') {
                
                // =========================================================
                // LÓGICA 1: RENDERIZAR A TABELA DE HISTÓRICO (TABELA 1)
                // =========================================================
                const tabelaTodos = document.getElementById('tabela-todos-veiculos');
                tabelaTodos.innerHTML = ''; // Limpa a tabela antes de preencher

                if (data.todos_veiculos.length === 0) {
                    tabelaTodos.innerHTML = `<tr><td colspan="3" class="text-center text-muted">Nenhum veículo cadastrado no sistema.</td></tr>`;
                } else {
                    data.todos_veiculos.forEach(veiculo => {
                        tabelaTodos.innerHTML += `
                            <tr>
                                <td><strong>#${veiculo.id}</strong></td>
                                <td><span class="badge bg-secondary font-monospace">${veiculo.placa}</span></td>
                                <td>${veiculo.modelo}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm" onclick="deletarVeiculo(${veiculo.id})">
                                        <i class="bi bi-trash"></i> Deletar Veiculo
                                    </button>
                                    <button class="btn btn-success btn-sm" onclick="ocuparVaga(${veiculo.id})">
                                        <i class="bi bi-car-front-fill"></i> Ocupar Vaga
                                    </button>
                                </td>
                            </tr>
                        `;
                    });
                }

                // =========================================================
                // LÓGICA 2: RENDERIZAR O GRID DE VAGAS FISICAS (TABELA 2)
                // =========================================================
                const gridEstacionamento = document.getElementById('grid-estacionamento');
                gridEstacionamento.innerHTML = ''; // Limpa o grid anterior
                
                let totalOcupadas = 0;
                const totalVagasPatio = 10; // Limite máximo do seu pátio

                // Renderiza os cards das vagas ocupadas dinamicamente
                data.vagas_ocupadas.forEach(vaga => {
                    totalOcupadas++;
                    gridEstacionamento.innerHTML += `
                        <div class="col">
                            <div class="card text-center bg-danger text-white h-100 shadow-sm border-0">
                                <div class="card-body py-3 d-flex flex-column justify-content-between">
                                    <div>
                                        <h5 class="card-title mb-1 small fw-bold">Vaga Ocupada</h5>
                                        <i class="bi bi-car-front-fill display-6 my-1 d-block"></i>
                                        <span class="badge bg-white text-danger font-monospace my-1">${vaga.placa}</span>
                                        <p class="card-text small mb-0 text-truncate" title="${vaga.modelo}">${vaga.modelo}</p>
                                    </div>
                                    <button class="btn btn-light btn-sm text-danger fw-bold mt-3 w-100" onclick="DesocuparVaga(${vaga.id})">
                                        Desocupar Vaga
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                });

                // Preenche o restante das vagas disponíveis até completar o limite de 10
                const vagasLivres = totalVagasPatio - totalOcupadas;
                for (let i = 0; i < vagasLivres; i++) {
                    gridEstacionamento.innerHTML += `
                        <div class="col">
                            <div class="card text-center bg-success text-white h-100 shadow-sm border-0">
                                <div class="card-body py-4">
                                    <h5 class="card-title mb-1 small fw-bold">Vaga Livre</h5>
                                    <i class="bi bi-p-circle display-6 my-2 d-block"></i>
                                    <p class="card-text small mb-0 fw-light">Disponível</p>
                                </div>
                            </div>
                        </div>
                    `;
                }

                // Atualiza o contador de vagas no topo da página
                const elementoContador = document.getElementById('total-ocupadas');
                if (elementoContador) {
                    elementoContador.textContent = totalOcupadas;
                }

            } else {
                // Esse else agora pertence corretamente ao "if (data.status === 'sucesso')"
                alert('Erro do servidor: ' + data.mensagem);
            }
        })
        .catch(error => {
            console.error('Erro na requisição AJAX:', error);
            alert('Não foi possível conectar ao servidor para carregar o estacionamento.');
        });
}
async function ocuparVaga(veiculo_id) {
    try {
        // Usando aspas simples normais e o sinal de "+" para juntar o ID
        const resposta = await fetch('/api/vagas/ocupar/' + veiculo_id + '/', {
            method: 'POST'
        });

        const resultado = await resposta.json();
        
        if (resultado.status === 'sucesso') {
            alert(resultado.mensagem);
            carregarVeiculos(); // Atualiza a tabela e o grid de vagas
        } else {
            alert("Erro: " + resultado.mensagem);
        }
    } catch (erro) {
        console.error("Erro ao ocupar vaga:", erro);
    }
}


async function DesocuparVaga(vaga_id) {
    try {
        const resposta = await fetch(`/api/vagas/liberar/${vaga_id}/`, {
            method: 'DELETE'
        });

        const resultado = await resposta.json();
        
        if (resultado.status === 'sucesso') {
            alert(resultado.mensagem);
            // Atualiza a tabela após deletar o veículo
            carregarVeiculos();
        } else {
            alert("Erro: " + resultado.mensagem);
        }
    } catch (erro) {
        console.error("Erro ao deletar veículo:", erro);
    }
}

// 2. FUNÇÃO PARA ADICIONAR (POST)
async function adicionarVeiculo() {
    const placaInput = document.getElementById('placa').value;
    const modeloInput = document.getElementById('modelo').value;

    const corpoRequisicao = {
        placa: placaInput,
        modelo: modeloInput
    };

    try {
        const resposta = await fetch('/api/veiculos/adicionar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(corpoRequisicao)
        });

        const resultado = await resposta.json();
        
        if (resultado.status === 'sucesso') {
            alert(resultado.mensagem);
            // Limpa os campos do formulário
            document.getElementById('placa').value = '';
            document.getElementById('modelo').value = '';
            // Atualiza a tabela com o novo dado do banco
            carregarVeiculos();
        } else {
            alert("Erro: " + resultado.mensagem);
        }
    } catch (erro) {
        console.error("Erro ao salvar veículo:", erro);
    }
}

async function deletarVeiculo(id) {
    try {
        const resposta = await fetch(`/api/veiculos/deletar/${id}/`, {
            method: 'DELETE'
        });

        const resultado = await resposta.json();
        
        if (resultado.status === 'sucesso') {
            alert(resultado.mensagem);
            // Atualiza a tabela após deletar o veículo
            carregarVeiculos();
        } else {
            alert("Erro: " + resultado.mensagem);
        }
    } catch (erro) {
        console.error("Erro ao deletar veículo:", erro);
    }
}

// Função auxiliar para obter o cookie CSRF padrão do Django
function obterCookie(nome) {
    let valorCookie = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, nome.length + 1) === (nome + '=')) {
                valorCookie = decodeURIComponent(cookie.substring(nome.length + 1));
                break;
            }
        }
    }
    return valorCookie;
}

async function enviarParaDjango() {
    const csrftoken = obterCookie('csrftoken');
    const dadosEnvio = { nome: "Lucas" };

    try {
        const resposta = await fetch("/api/mensagem/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken // Obrigatório para requisições POST no Django
            },
            body: JSON.stringify(dadosEnvio)
        });

        const resultado = await resposta.json();
        console.log(resultado);
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}
