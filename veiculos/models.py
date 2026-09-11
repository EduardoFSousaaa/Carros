from django.db import models

# Create your models here.
"""
Atributo placa: Um campo de texto (models.CharField) configurado como único.
● Atributo modelo: Um campo de texto (models.CharField).
● Método mágico: __str__ retornando o formato amigável.
Crie uma classe chamada VagaOcupada que representará as vagas em uso:
● Atributo veiculo: Uma chave estrangeira (models.ForeignKey) apontando para
Veiculo.
● Atributo data_entrada: Um campo de data/hora
(models.DateTimeField(auto_now_add=True))
"""

    
class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)

    def __str__(self):
        return self.modelo

class VagaOcupada(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vaga ocupada pelo veículo: {self.veiculo}"