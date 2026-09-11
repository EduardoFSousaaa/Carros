"""
URL configuration for Carro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from veiculos import views

urlpatterns = [ 
 path('admin/', admin.site.urls),
 # path('', include('veiculos.urls')),
    path('', views.home, name='veiculos'), # Abre a página inicial
    path('api/veiculos/', views.listar_veiculos_api, name='listar_veiculos'),
    path('api/veiculos/adicionar/', views.adicionar_veiculo_api, name='adicionar_veiculo'),
    path('api/veiculos/deletar/<int:veiculo_id>/', views.remover_veiculo_api, name='deletar_veiculo'),
    path('api/vagas/ocupar/<int:id>/', views.ocupar_vaga_api, name='ocupar_vaga'),
    path('api/vagas/liberar/<int:id>/', views.liberar_vaga_api, name='liberar_vaga'),
    path('api/vagas/ocupadas/', views.listar_vagas_ocupadas_api, name='listar_vagas_ocupadas'),
]
