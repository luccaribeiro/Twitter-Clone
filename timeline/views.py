from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import Profile, Tweet, Comentarios
from .forms import PostForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def principal (request):
    tweets = Tweet.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            usuario = request.user
            usuario_perfil = Profile.objects.get(user=usuario.id)
            post.user = usuario_perfil
            post.save()
            return redirect('main:timeline_page')
    else:
        form = PostForm()
    context = {'tweets': tweets, 'form': form }
    return render(request, 'timeline/principal.html', context)

def postagem(request, id):
    postagem_ref = Tweet.objects.get(id=id)
    reply_list = Tweet.objects.filter(reply_to=postagem_ref.id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            usuario = request.user
            usuario_perfil = Profile.objects.get(user=usuario.id)
            post.user = usuario_perfil
            post.reply_to_id = postagem_ref.id
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    context = {'postagem_ref':postagem_ref, 'form': form, 'reply_list':reply_list }
    return render(request, 'timeline/postagem.html', context)

def perfil(request, username):
    usuario = User.objects.get(username=username)
    usuario_perfil = Profile.objects.get(user=usuario.id)
    postagens = usuario_perfil.tweets.all()
    context = {'usuario':usuario, 'postagens':postagens, 'usuario_perfil':usuario_perfil}
    return render(request, 'timeline/perfil.html', context)