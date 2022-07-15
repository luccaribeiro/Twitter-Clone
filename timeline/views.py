from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import Tweet
from .forms import PostForm

def principal (request):
    tweets = Tweet.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('main:timeline_page')
    else:
        form = PostForm()
    context = {'tweets': tweets, 'form': form }
    return render(request, 'timeline/principal.html', context)
