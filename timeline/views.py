from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from GoogleNews import GoogleNews

from main.models import Profile, Reply, Tweet, Retweet

from .forms import ProfileForm, PostForm, RtForm, ReplyForm

googlenews = GoogleNews()
googlenews = GoogleNews(period="d")
googlenews = GoogleNews(lang="pt", region="BR")
googlenews.search("Brasil")


def principal(request):
    noticias = googlenews.results()
    tweets_query = list(Tweet.objects.all())
    rts = list(Retweet.objects.all())

    tweets = []
    for post in tweets_query + rts:
        tweets.append(post)
    tweets.sort(key=lambda x: x.created_on, reverse=True)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = Profile.objects.get(user=request.user.id).id
            post.save()
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
    reply_list = Reply.objects.filter(reference_tweet=postagem_ref.id).order_by('created_on')

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = int(Profile.objects.get(user=request.user.id).id)
            post.reference_tweet_id = id
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = ReplyForm()
    context = {
        "postagem_ref": postagem_ref,
        "form": form,
        "reply_list": reply_list,
        "noticias": noticias,
    }
    return render(request, "timeline/postagem.html", context)


def repost(request, id):
    ref_tweet = Tweet.objects.get(id=id)
    if request.method == 'POST':
        form = RtForm(request.POST)
        if form.is_valid():
            rt = form.save(commit=False)
            rt.user_id = Profile.objects.get(user_id=request.user.id).id
            rt.original_tweet_id = id
            rt.save()
            return redirect('timeline_page')
    else:
        form = RtForm()
    context = {
        'ref_tweet': ref_tweet,
        'form': form
    }
    return render(request, "timeline/repost.html", context)


def perfil(request, username):
    usuario_perfil = Profile.objects.get(user=User.objects.get(username=username).id)
    tweets_query = list(Tweet.objects.filter(user=usuario_perfil.id))
    rts = list(Retweet.objects.filter(user=usuario_perfil.id))

    postagens = []
    for post in tweets_query + rts:
        postagens.append(post)
    postagens.sort(key=lambda x: x.created_on, reverse=True)
    context = {
        "postagens": postagens,
        "usuario_perfil": usuario_perfil,
    }
    return render(request, "timeline/perfil.html", context)


def edit_perfil(request, username):
    usuario_perfil = Profile.objects.get(user=User.objects.get(username=username).id)
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
