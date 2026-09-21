import json
from django.http import JsonResponse
from django.template.backends import django
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Veiculo, VagaOcupada  # Importa o modelo baseado no seu crud.py
from crud import listarVeiculos, adicionarVeiculo, removerVeiculo, listarVagasOcupadas, liberarVaga
# VIEW 1: Retorna a página HTML principal
def home(request):
    from django.shortcuts import render
    QuantidadeVagas = 10  # Defina a quantidade total de vagas
    return render(request, 'home.html', {'QuantidadeVagas': QuantidadeVagas})

def listar_estacionamento_api(request):
    if request.method == 'GET':
        # 1. Busca todos os veículos da Tabela 1
        todos_veiculos = Veiculo.objects.all()
        dados_veiculos = [
            {'id': v.id, 'placa': v.placa, 'modelo': v.modelo} 
            for v in todos_veiculos
        ]
        
        # 2. Busca todas as vagas ocupadas da Tabela 2
        vagas_ocupadas = VagaOcupada.objects.all()
        dados_vagas = [
            {
                'id': vaga.id,
                'placa': vaga.veiculo.placa,  # Pega a placa através do relacionamento
                'modelo': vaga.veiculo.modelo
            }
            for vaga in vagas_ocupadas
        ]
        
        # Retorna as duas tabelas no JSON
        return JsonResponse({
            'status': 'sucesso', 
            'todos_veiculos': dados_veiculos,
            'vagas_ocupadas': dados_vagas
        })
        
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

# VIEW 3: Endpoint para Adicionar Veículo (Equivalente ao adicionarVeiculo do crud.py)
@csrf_exempt  # Ignora o CSRF para seu teste rápido
def adicionar_veiculo_api(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            placa = dados.get('placa')
            modelo = dados.get('modelo')

            if not placa or not modelo:
                return JsonResponse({'status': 'erro', 'mensagem': 'Campos obrigatórios ausentes'}, status=400)

            # Criação no banco idêntica ao seu script
            veiculo = Veiculo.objects.create(placa=placa, modelo=modelo)

            return JsonResponse({
                'status': 'sucesso', 
                'mensagem': 'Veículo cadastrado!',
                'veiculo': {'id': veiculo.id, 'placa': veiculo.placa, 'modelo': veiculo.modelo}
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido'}, status=400)
            
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
@csrf_exempt 
def remover_veiculo_api(request, veiculo_id):
    if request.method == 'DELETE':
        try:
            veiculo = Veiculo.objects.get(id=veiculo_id)
            veiculo.delete()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Veículo removido!'})
        except Veiculo.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Veículo não encontrado'}, status=404)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

def verificarExistemVagaLivre():
    VAGAS_TOTAIS = 10
    intVagasOcupadas = VagaOcupada.objects.all().count()
    "return booleano - se existem vagas livres"
    return intVagasOcupadas < VAGAS_TOTAIS
@csrf_exempt 
def ocupar_vaga_api(request, veiculo_id):
    # 1. Garante que só aceita requisições POST
    if request.method != 'POST':
        return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
    try:
        # 2. Busca o veículo diretamente pelo ID recebido na URL
        veiculo = Veiculo.objects.filter(id=veiculo_id).first()
        if not veiculo:
            return JsonResponse({'status': 'erro', 'mensagem': 'Veículo não encontrado no histórico'}, status=404)

        if verificarExistemVagaLivre():
        # 3. Impede que o mesmo carro ocupe duas vagas ao mesmo tempo
            if VagaOcupada.objects.filter(veiculo=veiculo).exists():
                return JsonResponse({'status': 'erro', 'mensagem': 'Este veículo já está estacionado em uma vaga ativa.'}, status=400)
             # 5. Salva na tabela vinculando a vaga ao carro correspondente
            vagaoc = VagaOcupada.objects.create(
                veiculo=veiculo,
                data_entrada=timezone.now()
            )
            return JsonResponse({
                        'status': 'sucesso', 
                        'mensagem': 'Veículo estacionado com sucesso}!',
                        'dados_vaga': {
                            'id': vagaoc.id,
                            'placa': veiculo.placa,
                            'modelo': veiculo.modelo,
                            'data_entrada': vagaoc.data_entrada.strftime('%d/%m/%Y %H:%M')
                        }
                    }, status=201)
        # Se não houver vaga disponível, barra a entrada
        else:
            return JsonResponse({'status': 'erro', 'mensagem': 'Estacionamento lotado! Não há vagas livres.'}, status=400)
        

    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': f'Erro interno no servidor: {str(e)}'}, status=500)
@csrf_exempt
def liberar_vaga_api(request, vaga_id):
    try:
        vaga_ocupada = VagaOcupada.objects.get(id=vaga_id)
        vaga_ocupada.delete()
        return JsonResponse({'status': 'sucesso', 'mensagem': 'Vaga liberada!'})
    except VagaOcupada.DoesNotExist:
        return JsonResponse({'status': 'erro', 'mensagem': 'Vaga não encontrada'}, status=404)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
@csrf_exempt
def listar_vagas_ocupadas_api(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)

            # Criação no banco idêntica ao seu script
            listarVagasOcupadas = VagaOcupada.objects.all()
    
            return JsonResponse({
                'status': 'sucesso', 
                'mensagem': 'Lista Vagas Ocupadas',
                'vagas': [{'id': vaga.id, 'placa': vaga.placa, 'modelo': vaga.modelo, 'data_entrada': vaga.data_entrada} for vaga in listarVagasOcupadas]
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido'}, status=400)       
        return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)


