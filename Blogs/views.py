from django.core.urlresolvers import reverse
from django.shortcuts import render
from Blogs.models import Post, Comment
from Blogs.forms import AnonymousUserCommentForm, UserCommentForm
from django.http import HttpResponseRedirect

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
    single_post = Post.objects.get(id=post_id)
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
                                                                  "comments": comments})
    else:
        form = AnonymousUserCommentForm()
        if request.POST:
            form = AnonymousUserCommentForm(request.POST)
            if form.is_valid():
                form.save(post=single_post)
            else:
                return render(request, 'Blogs/single_post.html', {"post": single_post,
                                                                  "form": form,
                                                                  "comments": comments})
    return render(request, 'Blogs/single_post.html', {"post": single_post,
                                                      "form": form,
                                                      "comments": comments})


def email_activation(request, key):
    Comment.objects.filter(activation_key=key).update(approved=True)
    return HttpResponseRedirect(reverse("index"))


def handler_404(request):
    return render(request, "Error/404.html")


def handler_500(request):
    return render(request, "Error/500.html")