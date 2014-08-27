import hashlib
import random
from time import timezone
import uuid
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template.loader import render_to_string
from Blogs.models import Post, Comment
from Blogs.forms import AnonymousUserCommentForm, UserCommentForm
from django.http import HttpResponseRedirect, HttpResponse
import task


def index(request, **kwargs):
    start_index = 0
    last_index = 3
    context = {}
    if 'page_index' in kwargs:
        start_index = last_index * int(kwargs["page_index"])
        last_index += start_index
        context["page_index"] = kwargs["page_index"]
        context["prev"] = int(kwargs["page_index"]) - 1
        context["next"] = int(kwargs["page_index"]) + 1
    else:
        context["prev"] = 0
        context["next"] = 1
    post_list = Post.objects.all().order_by("-date")[start_index:last_index]
    context['post_list'] = post_list

    return render(request, 'Blogs/index.html', context)


def post(request, post_id):
    temp_post = cache.get(post_id)
    if temp_post:
        single_post = temp_post
    else:
        single_post = Post.objects.get(id=post_id)
        cache.set(post_id, single_post, timeout=None)
    comments = single_post.comment.filter(approved=True)
    if request.user.is_authenticated():
        form = UserCommentForm()
        if request.POST:
            form = UserCommentForm(request.POST)
            if form.is_valid():
                form.save(user=request.user, post=single_post)
            else:
                return render(request, 'Blogs/single_post.html', {"post": single_post,
                                                                  "form": form,
                                                                  "comments": comments,
                                                                  "request": request})
    else:
        form = AnonymousUserCommentForm()
        if request.POST:
            form = AnonymousUserCommentForm(request.POST)
            if form.is_valid():
                form.save(post=single_post)
            else:
                return render(request, 'Blogs/single_post.html', {"post": single_post,
                                                                  "form": form,
                                                                  "comments": comments,
                                                                  "request": request})
    return render(request, 'Blogs/single_post.html', {"post": single_post,
                                                      "form": form,
                                                      "comments": comments,
                                                      "request": request})


def sub_comment_add(request, comment_id):
    if request.user.is_authenticated():

        comment = Comment.objects.get(id=comment_id)
        new_comment = Comment(content=request.POST["content"],
                              author=request.user,
                              approved=True,
                              activation_key=0,
                              content_object=comment,
                              email=request.user.email
                              )
        new_comment.save()
    else:
        user = User.objects.get(email=request.POST["email"])
        if not user:
            user = User.objects.create_user(username=uuid.uuid4(),
                                            email=request.POST["email"],
                                            is_active=False)

        comment = Comment()
        comment.content = request.POST["content"]
        comment.author = user
        comment.date = timezone.now()
        comment.approved = False
        comment.email = user.email
        comment.content_object = post
        comment.activation_key = hashlib.sha256(user.email + str(random.random())).hexdigest()
        comment.save()
        content = render_to_string("Email/email.html", {"activation_key": comment.activation_key})
        task.mail_send.delay("Email Activation", content, None, [comment.email])

    return HttpResponseRedirect(request.GET["next"])


def email_activation(request, key):
    Comment.objects.filter(activation_key=key).update(approved=True)
    return HttpResponseRedirect(reverse("index"))


def handler_404(request):
    return render(request, "Error/404.html")


def handler_500(request):
    return render(request, "Error/500.html")