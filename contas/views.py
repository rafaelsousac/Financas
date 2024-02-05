from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime


def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    titulo = request.POST.get('titulo')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    valor = request.POST.get('valor')
    dia_pagamento = request.POST.get('dia_pagamento')

    conta = ContaPagar(
        titulo=titulo,
        categoria_id=categoria,
        descricao=descricao,
        valor=valor,
        dia_pagamento=dia_pagamento
    )
    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/contas/definir_contas')


def ver_contas(request):
    mes_atual = datetime.now().month
    dia_atual = datetime.now().day

    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=mes_atual).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=dia_atual).exclude(id__in=contas_pagas)

    contas_proximas_vencimento = (contas.filter(dia_pagamento__lte=dia_atual + 7).filter(dia_pagamento__gt=dia_atual).exclude(id__in=contas_pagas))

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento).exclude(id__in=contas_pagas)

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas,
                                                                  'contas_proximas_vencimento': contas_proximas_vencimento,
                                                                  'restantes': restantes})



