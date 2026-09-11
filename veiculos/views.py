import json
from django.http import JsonResponse
from django.template.backends import django
from django.views.decorators.csrf import csrf_exempt
from .models import Veiculo, VagaOcupada  # Importa o modelo baseado no seu crud.py
from crud import listarVeiculos, adicionarVeiculo, removerVeiculo, listarVagasOcupadas, liberarVaga
# VIEW 1: Retorna a página HTML principal
def home(request):
    from django.shortcuts import render
    return render(request, 'home.html')

# VIEW 2: Endpoint para Listar Veículos (Equivalente ao listarVeiculos do crud.py)
def listar_veiculos_api(request):
    if request.method == 'GET':
        veiculos = Veiculo.objects.all()
        # Transforma o QuerySet em uma lista de dicionários para o JSON
        dados = [
            {'id': v.id, 'placa': v.placa, 'modelo': v.modelo} 
            for v in veiculos
        ]
        return JsonResponse({'status': 'sucesso', 'veiculos': dados})
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
def remover_veiculo_api(request, id):
    if request.method == 'DELETE':
        try:
            veiculo = Veiculo.objects.get(id=id)
            veiculo.delete()
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Veículo removido!'})
        except Veiculo.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Veículo não encontrado'}, status=404)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
def ocupar_vaga_api(request, id):
 if request.method == 'POST':
    try:
        dados = json.loads(request.body)
        placa = dados.get('placa')
        modelo = dados.get('modelo')

        if not placa or not modelo:
            return JsonResponse({'status': 'erro', 'mensagem': 'Campos obrigatórios ausentes'}, status=400)

        # Criação no banco idêntica ao seu script
        vagaoc = VagaOcupada.objects.create(placa=placa, modelo=modelo,data_entrada=django.utils.timezone.now() )

        return JsonResponse({
            'status': 'sucesso', 
            'mensagem': 'Veículo cadastrado!',
            'veiculo': {'id': vagaoc.id, 'placa': vagaoc.placa, 'modelo': vagaoc.modelo, 'data_entrada': vagaoc.data_entrada}
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido'}, status=400)       
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
def liberar_vaga_api(request, id):
    # Lógica para liberar uma vaga ocupada com o ID fornecido
    pass
def listar_vagas_ocupadas_api(request):
    # Lógica para listar todas as vagas ocupadas
    pass    

