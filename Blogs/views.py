from django.shortcuts import render


def index(request):
    return render(request, 'Blogs/index.html', '')


def post(request, post_id):
    return render(request, 'Blogs/single_post.html', '')