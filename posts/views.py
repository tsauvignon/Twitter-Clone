
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import Postform
from .models import Post
from cloudinary.forms import cl_init_js_callbacks
from django.urls import reverse_lazy, reverse
# Create your views here.


def index(request):
    # If the method is POST
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        # If the form is valid
        if form.is_valid():
            # yes save
            form.save()

            # redirect to home
            return HttpResponseRedirect('/')
        else:
            # no show error
            return HttpResponseRedirect(form.errors.as_json)

    posts = Post.objects.all().order_by('-created_at')[:20]

    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    # Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def update(request, post_id):
    # If the method is POST
    post = Post.objects.get(id=post_id)

    # if request file is there return tweets
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES, instance=post)
        # If the form is valid
        if form.is_valid():
            # Yes, Save
            form.save()
            # save and reddirect to home page
            return HttpResponseRedirect('/')
    # if we want to update then it will redirect back to the update.html it will display to user
    else:
        form = Postform
        return render(request, 'update.html', {'post': post, 'form': form})


def like(request, post_id):
    # Find Post
    post = Post.objects.get(id=post_id)
    newlikecount = post.like_count+1
    post.like_count = int(newlikecount)
    post.save()
    return HttpResponseRedirect('/')
