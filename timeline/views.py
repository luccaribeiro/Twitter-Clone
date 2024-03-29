from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from GoogleNews import GoogleNews

from main.models import Like, Profile, Relationship, Tweet, Notification

from .forms import PostForm, ProfileForm

googlenews = GoogleNews()
googlenews = GoogleNews(period='d')
googlenews = GoogleNews(lang='pt', region='BR')
googlenews.search('BRASIL')
noticias = googlenews.results()


def get_tweets(user_id):
    return Tweet.objects.filter(
        Q(user_id=user_id) | Q(
            user__id__in=Relationship.objects.filter(user_id=user_id).values_list('follower_id', flat=True)
        )
    ).order_by('-created_on')


def principal(request):
    user_profile = Profile.objects.get(user=request.user)
    tweets = get_tweets(user_profile)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.content:
                post.user_id = request.user.profile.id
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
            post.user_id = request.user.profile.id
            post.reply_to_id = id
            post.num_type = 2
            if post.content:
                post.save()
                Notification.objects.create(user=postagem_ref.user,
                                            tweet_ref=postagem_ref,
                                            author=request.user.profile,
                                            notification_type='respondeu seu tweet')

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
            rt.user_id = request.user.profile.id
            rt.num_type = 1
            rt.retweets_the_id = id
            rt.save()
            Notification.objects.create(user=ref_tweet.user,
                                        tweet_ref=ref_tweet,
                                        author=request.user.profile,
                                        notification_type='retweetou seu tweet')
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
    usuario_logado = request.user.profile.id
    usuario_perfil = Profile.objects.get(user=User.objects.get(username=username).id)

    postagens = Tweet.objects.filter(user=usuario_perfil.id).filter(
        reply_to__isnull=True).order_by('-created_on')

    seguindo = Relationship.objects.filter(follower_id=usuario_perfil.id).count()
    seguidores = Relationship.objects.filter(user_id=usuario_perfil.id).count()
    deixar_de_seguir = Relationship.objects.filter(follower=usuario_logado, user=usuario_perfil).exists()
    context = {
        "postagens": postagens,
        "usuario_perfil": usuario_perfil,
        "noticias": noticias,
        "seguidores": seguidores,
        "seguindo": seguindo,
        "deixar_de_seguir": deixar_de_seguir,
        "usuario_logado": usuario_logado
    }

    return render(request, "timeline/perfil.html", context)


def edit_perfil(request, username):
    usuario_perfil = Profile.objects.get(
        user=User.objects.get(username=username).id)
    postagens = Tweet.objects.filter(user_id=usuario_perfil.id).order_by('-created_on')
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=usuario_perfil)
        if form.is_valid():
            form.save()
            return redirect(reverse("perfil", args=[usuario_perfil.user.username]))
    else:
        form = ProfileForm(initial={
            'nickname': usuario_perfil.nickname,
            'avatar': usuario_perfil.avatar,
            'capa': usuario_perfil.capa,
            'bio': usuario_perfil.bio
        })
    context = {
        "postagens": postagens,
        "usuario_perfil": usuario_perfil,
        "form": form,
    }
    return render(request, "timeline/perfil_edit.html", context)


# def like(request, id):
#     try:
#         tweet_like = Like(user=Profile.objects.get(
#             user=request.user.id), tweet=Tweet.objects.get(id=id))
#         tweet_like.save()
#     except IntegrityError:
#         like_delete = Like.objects.get(user=Profile.objects.get(
#             user=request.user.id), tweet=Tweet.objects.get(id=id))
#         like_delete.delete()
#     return redirect('timeline_page')


def api_like(request, id):
    tweet_like = get_object_or_404(Tweet, id=id)
    try:
        Like.objects.create(user=request.user.profile, tweet=tweet_like)
        Notification.objects.create(user=tweet_like.user, tweet_ref=tweet_like, author=request.user.profile)
        resposta = {
            'like': True
        }
    except IntegrityError:
        Like.objects.get(user=request.user.profile, tweet=tweet_like).delete()
        resposta = {
            'like': False
        }
    resposta['likes_count'] = tweet_like.like.count()
    return JsonResponse(resposta)


def notifications(request):
    return JsonResponse(
        {
            'alerts': Notification.objects.filter(user=request.user.profile, viewed=False).count()
        }
    )


def notification_viewed(request):
    Notification.objects.filter(user=request.user.profile, viewed=False).update(viewed=True)
    return redirect('open_notification')


def open_notification(request):
    notificacoes = Notification.objects.filter(user=request.user.profile).order_by('-created_on')
    context = {
        'notificacoes': notificacoes
    }
    return render(request, 'timeline/notificacao.html', context)


def follow(request, username):
    current_user = request.user.profile
    to_user = User.objects.get(username=username).profile
    Relationship(follower=current_user, user=to_user).save()
    Notification.objects.create(user=to_user, author=request.user.profile, notification_type='agora segue você!')
    return redirect('timeline_page')


def unfollow(request, username):
    current_user = request.user.profile
    to_user = User.objects.get(username=username).profile
    Relationship.objects.get(
        follower=current_user.id, user=to_user).delete()
    return redirect('timeline_page')
