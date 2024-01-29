from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total


def home(request):
    contas = Conta.objects.all()
    total_contas = calcula_total(contas, 'valor')
    return render(request, 'home.html', {'contas': contas, 'total_contas': total_contas})


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = calcula_total(contas, 'valor')
    return render(request, 'gerenciar.html', {'contas': contas, 'categorias': categorias,
                                                                 'total_contas': total_contas})


def cadastrar_banco(request):
    if request.POST:
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')

        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/perfil/gerenciar/')
        conta = Conta(
            apelido=apelido,
            banco=banco,
            tipo=tipo,
            valor=valor,
            icone=icone
        )
        conta.save()
        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    if request.POST:
        nome = request.POST.get('categoria')
        essencial = bool(request.POST.get('essencial'))

        if len(nome.strip()) == 0 or not (isinstance(essencial, bool)):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/perfil/gerenciar/')

        categoria = Categoria(
            categoria=nome,
            essencial=essencial,
        )
        categoria.save()
        messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
        return redirect('/perfil/gerenciar/')


def atualizar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not(categoria.essencial)
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Tipo de categoria alterado com sucesso')
    return redirect('/perfil/gerenciar/')