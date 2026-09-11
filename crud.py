import os
import django
from django.views.decorators.csrf import csrf_exempt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carro.settings')
django.setup()

from veiculos.models import Veiculo, VagaOcupada

"Create veiculo"
def adicionarVeiculo():
    placa = input("Placa: ")
    modelo = input("Modelo: ")

    Veiculo.objects.create(
        placa=placa,
        modelo=modelo
    )

    print("Veículo cadastrado!")
"listar veiculos"
def listarVeiculos():
    veiculos = Veiculo.objects.all()

    print("\n--- VEÍCULOS ---")

    for veiculo in veiculos:
        print(
            f"{veiculo.id} - "
            f"{veiculo.placa} - "
            f"{veiculo.modelo}"
        )
"remover veiculo"
def removerVeiculo(id):
    veiculo = Veiculo.objects.get(id=id)
    veiculo.delete()

    print("Veículo removido!")

"listar vagas ocupadas"
def listarVagasOcupadas():
    vagas_ocupadas = VagaOcupada.objects.all()
    return vagas_ocupadas
    """print("\n--- VAGAS OCUPADAS ---")

    for vaga in vagas_ocupadas:
        print(
            f"ID: {vaga.id} - "
            f"Veículo: {vaga.veiculo.modelo} - "
            f"Placa: {vaga.veiculo.placa} - "
            f"Data de entrada: {vaga.data_entrada}"
        )"""
"Remover veiculo da vaga"
def liberarVaga():
    id = int(input("ID da vaga ocupada: "))
    if not VagaOcupada.objects.filter(id=id).exists():
        print("Vaga ocupada não encontrada.")
        return 
    vaga_ocupada = VagaOcupada.objects.get(id=id)
    vaga_ocupada.delete()

    print("Vaga liberada!")

"adicinoar veiculo a vaga"
def ocuparVaga():
    if verificarExistemVagaLivre():
        id = int(input("ID do veículo: "))
        veiculo = Veiculo.objects.get(id=id)
        data = django.utils.timezone.now()

        VagaOcupada.objects.create(
            veiculo=veiculo,
            data_entrada=data
        )

        print("Vaga ocupada!")
    else:
        print("Não há vagas disponíveis.")
def verificarExistemVagaLivre():
    VAGAS_TOTAIS = 10
    intVagasOcupadas = VagaOcupada.objects.all().count()
    "return booleano - se existem vagas livres"
    return intVagasOcupadas < VAGAS_TOTAIS
