#Eduardo Frtisch Sousa
#Matricula:201520196
import pytest
#Estacionamento: 10 vagas, sem placas duplicadas. 
#Melhore o código sem alterar suas regras.
def estacionar_veiculo(placas_Veiculos,Nova_Placa_Veiculo):
    Vagas_Totais = 10;
    # Guard Clause 1: Verifica se o veículo já está estacionado
    if not (Nova_Placa_Veiculo not in placas_Veiculos):
        return "Veículo já estacionado"
    # Guard Clause 2: Verifica se o estacionamento já está lotado
    if not ha_vaga_disponivel(len(placas_Veiculos), Vagas_Totais):
        return "Estacionamento lotado"
    # Fluxo principal (Caminho feliz): Executado apenas se as guardas passarem
    placas_Veiculos.append(Nova_Placa_Veiculo);
    return "Entrada registrada"

#Crie ha_vaga_disponivel: receba quantidade e capacidade; retorne True/False sem alterar a lista.
def ha_vaga_disponivel(quantidade, capacidade):
    # Guard Clause: Verifica se há vagas disponíveis
    if quantidade >= capacidade:
        return False
    return True

def test_Cenario_NovaPlaca_vagaLivre():
    vagas_Ocupadas = ["ABC1234", "DEF5678", "GHI9012"]
    placa_Veiculo = "JKL3456"
    resultado = estacionar_veiculo(placas_Veiculos=vagas_Ocupadas, Nova_Placa_Veiculo=placa_Veiculo)
    assert resultado == "Entrada registrada"
    assert placa_Veiculo in vagas_Ocupadas
    
def test_Cenario_PlacaDuplicada():
    vagas_Ocupadas = ["ABC1234", "DEF5678", "GHI9012"]
    placa_Veiculo = "ABC1234"
    resultado = estacionar_veiculo(placas_Veiculos=vagas_Ocupadas, Nova_Placa_Veiculo=placa_Veiculo)
    assert resultado == "Veículo já estacionado"
    assert vagas_Ocupadas.count(placa_Veiculo) == 1

def test_Cenario_EstacionamentoLotado():
    vagas_Ocupadas = ["ABC1234", "DEF5678", "GHI9012", "JKL3456", "MNO7890",
                       "PQR1234", "STU5678", "VWX9012", "YZA3456", "BCD7890"]
    placa_Veiculo = "EFG1234"
    resultado = estacionar_veiculo(placas_Veiculos=vagas_Ocupadas, Nova_Placa_Veiculo=placa_Veiculo)
    assert resultado == "Estacionamento lotado"
    assert placa_Veiculo not in vagas_Ocupadas

# EXECUTA OS TESTES EM TERMINAL: pytest estacionamento.py

""" A)Pontos de melhorias do codigo inicial:
# Nome de variaveis errados p e v
# if que estava em cascata, foi transformado em guard clauses
# Constante ao inves de capacidade total ser um valor direto no if sem Comentario e sem regra de negocio clara

Justificativa: O código inicial tinha problemas de legibilidade e clareza, com nomes de variáveis pouco descritivos e
 estruturas de controle que dificultavam a compreensão.
A refatoração introduziu guard clauses para simplificar a lógica, melhorou os nomes das variáveis para refletir melhor seu propósito e 
utilizou uma constante para a capacidade total do estacionamento, tornando o código mais fácil de entender e manter e melhorando sua legibilidade.
"""