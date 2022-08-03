from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from GoogleNews import GoogleNews
from main.models import Like, Profile, Relationship, Tweet

from .forms import PostForm, ProfileForm

googlenews = GoogleNews()
googlenews = GoogleNews(period="d")
googlenews = GoogleNews(lang="pt", region="BR")
googlenews.search("Brasil")


def principal(request):
    noticias = googlenews.results()
    tweets = Tweet.objects.filter(
        reply_to__isnull=True).order_by('-created_on')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.content:
                post.user_id = Profile.objects.get(user=request.user.id).id
                post.save()
                return redirect("main:timeline_page")
            else:
                messages.warning(request, "Por favor, preencha esse campo.")
                return redirect("main:timeline_page")

    else:
        form = PostForm()
    context = {
        "tweets": tweets,
        "form": form,
        "noticias": noticias,
    }
    return render(request, "timeline/principal.html", context)


def postagem(request, id):
    noticias = googlenews.results()
    postagem_ref = Tweet.objects.get(id=id)
    reply_list = Tweet.objects.filter(
        reply_to=postagem_ref.id).order_by('created_on')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = int(Profile.objects.get(user=request.user.id).id)
            post.reply_to_id = id
            post.num_type = 2
            if post.content:
                post.save()
                return HttpResponseRedirect(request.path_info)
            else:
                messages.warning(request, "Por favor, preencha esse campo.")
                return redirect(request.path_info)
    else:
        form = PostForm()

    retweetado = None
    if postagem_ref.retweets_the_id:
        retweetado = Tweet.objects.get(id=postagem_ref.retweets_the_id)
    context = {
        "postagem_ref": postagem_ref,
        "form": form,
        "reply_list": reply_list,
        "noticias": noticias,
        "retweetado": retweetado
    }
    return render(request, "timeline/postagem.html", context)


def repost(request, id):
    noticias = googlenews.results()
    ref_tweet = Tweet.objects.get(id=id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            rt = form.save(commit=False)
            rt.user_id = Profile.objects.get(user_id=request.user.id).id
            rt.num_type = 1
            rt.retweets_the_id = id
            rt.save()
            return redirect('timeline_page')
    else:
        form = PostForm()
    context = {
        'ref_tweet': ref_tweet,
        'form': form,
        'noticias': noticias
    }
    return render(request, "timeline/repost.html", context)


def perfil(request, username):
    usuario_perfil = Profile.objects.get(
        user=User.objects.get(username=username).id)
    seguindo = usuario_perfil.following
    postagens = Tweet.objects.filter(user=usuario_perfil.id).filter(
        reply_to__isnull=True).order_by('-created_on')

    context = {
        "postagens": postagens,
        "usuario_perfil": usuario_perfil,
        "seguindo": seguindo,
    }
    return render(request, "timeline/perfil.html", context)


def edit_perfil(request, username):
    usuario_perfil = Profile.objects.get(
        user=User.objects.get(username=username).id)
    postagens = usuario_perfil.tweets.all()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            usuario_perfil.nickname = post.nickname
            usuario_perfil.avatar = post.avatar
            usuario_perfil.capa = post.capa
            usuario_perfil.bio = post.bio
            usuario_perfil.save()
            return redirect(reverse("perfil", args=[usuario_perfil.user.username]))
    else:
        form = ProfileForm()
    context = {
        "postagens": postagens,
        "usuario_perfil": usuario_perfil,
        "form": form,
    }
    return render(request, "timeline/perfil_edit.html", context)


def like(request, id):
    try:
        tweet_like = Like(user=Profile.objects.get(
            user=request.user.id), tweet=Tweet.objects.get(id=id))
        tweet_like.save()
    except IntegrityError:
        like_delete = Like.objects.get(user=Profile.objects.get(
            user=request.user.id), tweet=Tweet.objects.get(id=id))
        like_delete.delete()
    return redirect('timeline_page')


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    return redirect('timeline_page')


def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.get(
        from_user=current_user.id, to_user=to_user_id)
    rel.delete()
    return redirect('timeline_page')
