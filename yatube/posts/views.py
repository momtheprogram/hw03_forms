from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Главная страница сайта Yatube'
    context = {
        'page_obj': page_obj,
        'title': title
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    context = {
        'group': group,
        'posts': posts,
        'page_obj': paginator.get_page(page_number)
    }
    template = 'posts/group_list.html'
    return render(request, template, context)

def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = User.objects.get(username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профайл пользователя {username}'
    all_posts = post_list.count()
    context = {
        'page_obj': page_obj,
        'title': title,
        'all_posts': all_posts,
        'author': author
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()
    #user_post = User.objects.get(pk=post_id)
    #print_post = Post.objects.filter(author__username = user_post)
    title_30 = post.text[:30]
    context = {
        'title': title_30,
        'post_count': posts_count,
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request,'posts/create_post.html', context)

@login_required
def post_edit(request, post_id):
    current_post = get_object_or_404(
        Post, pk=post_id
    )
    if request.user != current_post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None,
        instance=current_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'current_post': current_post
    }
    return render(request, 'posts/create_post.html', context )
