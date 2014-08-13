from django.shortcuts import render, render_to_response
from Blogs.models import Post
from Blogs.forms import AnonymousUserCommentForm, UserCommentForm
from django.contrib.contenttypes.models import ContentType


def index(request):
    post_list = Post.objects.all().order_by("-date")[:10]
    context = {'post_list': post_list}
    return render(request, 'Blogs/index.html', context)


def post(request, post_id):
    single_post = Post.objects.get(id=post_id)
    content_type = ContentType.objects.get_for_model(single_post)
    form = ""
    if request.method == "POST":
        if request.user.is_authenticated():
            form = UserCommentForm(request.POST, initial={"email": request.user.email,
                                                          "author": request.user,
                                                          "object_id": post_id
                                                          })
            form.has_changed()
        else:
            form = AnonymousUserCommentForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        if request.user.is_authenticated():
            form = UserCommentForm
        else:
            form = AnonymousUserCommentForm
    return render(request, 'Blogs/single_post.html', {'post': single_post, 'form': form})