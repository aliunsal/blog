import hashlib
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from Users.forms import UserPost, UserProfile as UserProfileForm, UserRegister
from Users.models import UserProfile
from Blogs.models import Post
from django.utils import timezone
import task


def user_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("user_index"))
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse("user_index"))
    return render(request, "Users/login.html", )


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required()
def index(request):
    #task.mail_send.delay("asdsaa", "ljasndlknsad", "Ali Unsal", ["aliunsal@live.com"])
    return render(request, "Users/index.html")


@login_required()
def user_post_list(request):
    post_list = Post.objects.filter(author=request.user)
    return render(request, "Users/post_list.html", {"post_list": post_list})


@login_required()
def user_post_remove(request, post_id):
    post = Post.objects.get(id=post_id)
    Post.delete(post)
    return HttpResponseRedirect(reverse("user_post_list"))


@login_required()
def user_post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user:
        return HttpResponseRedirect(reverse("user_post_list"))
    if request.POST:
        form = UserPost(request.POST, request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.content = form.cleaned_data["content"]
            if form.cleaned_data["picture"] and post.picture != form.cleaned_data["picture"]:
                post.picture = form.cleaned_data["picture"]
            post.save()
            task.resize_image.delay(post.picture.url, 636, 237)
        else:
            return render(request, "Users/post_edit.html", {"form": form})
    else:
        form = UserPost(initial={"title": post.title,
                                 "content": post.content,
                                 "picture": post.picture.url})
    return render(request, "Users/post_edit.html", {"form": form})


@login_required()
def user_post_add(request):
    if request.POST:
        form = UserPost(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = Post(title=form.cleaned_data["title"],
                            content=form.cleaned_data["content"],
                            date=timezone.now(),
                            picture=form.cleaned_data["picture"],
                            author=request.user
                            )
                post.save()
                task.resize_image.delay(post.picture.url, 636, 237)
            except Exception as e:
                return HttpResponse(str(e))
            return render(request, "Users/post_add.html", {"form": form})
        else:
            return render(request, "Users/post_add.html", {"form": form})
    else:
        form = UserPost()
    return render(request, "Users/post_add.html", {"form": form})



@login_required()
def user_profile(request):
    user = UserProfile.objects.get(user=request.user)
    if not request.POST:
        try:
            form = UserProfileForm(initial={"first_name": user.user.first_name,
                                            "last_name": user.user.last_name,
                                            "email": user.user.email,
                                            "avatar": user.avatar})
        except Exception as e:
            form = UserProfileForm()

        return render(request, "Users/profile.html", {"user": user,
                                                      "form": form})
    else:
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.user.first_name = form.cleaned_data["first_name"]
            user.user.last_name = form.cleaned_data["last_name"]

            if user.user.email != form.cleaned_data["email"]:
                user.user.email = form.cleaned_data["email"]
                user.activation_key = hashlib.sha256(user.email + str(random.random())).hexdigest()
                content = render_to_string("Email/email.html", {"activation_key": user.activation_key})
                task.mail_send.delay("Email Activation", content, None, [user.user.email])
                user.user.save()
            if form.cleaned_data["avatar"] and user.avatar != form.cleaned_data["avatar"]:
                user.avatar = form.cleaned_data["avatar"]

            try:
                user.save()
                user.user.save()
                task.resize_image.delay(user.avatar.url, 70, 70)
            except Exception as e:
                print e

            return render(request, "Users/profile.html", {"user": user,
                                                          "form": form})
        else:
            return render(request, "Users/profile.html", {"user": user,
                                                          "form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, "Users/register.html", {'form': form})
    else:
        form = UserRegister()
    return render(request, "Users/register.html", {
        'form': form,
    })


def user_activation(request,key):
    user_profile = UserProfile.objects.filter(activation_key=key)
    if user_profile:
        user_profile.user.is_active = True
        user_profile.user.save()

    return HttpResponseRedirect(reverse("index"))
