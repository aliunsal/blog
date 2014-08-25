from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from Users.forms import UserPost, UserProfile as UserProfileForm
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

        else:
            return render(request, "Users/post_add.html", {"form": form})
    else:
        form = UserPost()
        return render(request, "Users/post_add.html", {"form": form})
    return HttpResponse("hic bisey")


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
        form = UserProfileForm(request.POST)
        if form.is_valid():
            #user_profile = UserProfile(user=request.user,avatar=)
            return HttpResponse("")
        else:
            return HttpResponse(form.cleaned_data["email"])

    return HttpResponse("hic bisey")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "Users/register.html", {
        'form': form,
    })