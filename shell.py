from django.contrib.auth.models import Veiculo,VagaOcupada
import crud

for i in range(2):
    crud.ocuparVaga()
crud.listarVagasOcupadas()
crud.liberarVaga

""" link consulta
https://dev.to/_lvleo21/django-como-usar-o-shell--4npn
"""