from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

def blog_home(request):
    # 1. 获取所有文章（按发布时间倒序）
    post_list = Post.objects.all().order_by('-publish_time')
     # 给每个文章添加阅读时长属性
    for post in post_list:
        # 计算字数（无内容则为0）
        content_length = len(post.content) if post.content else 0
        # 阅读时长：向上取整，每分钟300字
        post.read_time = (content_length + 299) // 300  # 整数除法向上取整
    
    # 2. 配置分页：每页显示5篇文章（可自行修改数字）
    paginator = Paginator(post_list, 6)
    
    # 3. 获取当前页码（从URL参数?page=X中获取）
    page = request.GET.get('page')
    
    try:
        # 4. 获取当前页的文章列表
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是数字，默认显示第1页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        posts = paginator.page(paginator.num_pages)
    
    # 5. 把分页后的文章和分页器传给模板
    return render(request, 'blog/home.html', {
        'posts': posts,  # 当前页的文章列表
        'paginator': paginator  # 分页器对象（用于模板显示页码）
    })
def post_create(request):
    return render(request, "blog/create.html")

def post_detail(request, pk):
    # 1. 获取文章，不存在则返回404
    post = get_object_or_404(Post, pk=pk)
    
    # 2. 阅读量+1（纯整数操作，无拼接）
    post.views += 1  # 仅整数相加，无字符串参与
    post.save()
    
    # 3. 传递数据给模板
    return render(request, 'blog/detail.html', {'post': post})

def post_by_category(request, cate_id):
    return render(request, "blog/category.html")

def phome(request):
        # 1. 获取所有文章（按发布时间倒序）
    post_list = Post.objects.all().order_by('-publish_time')
     # 给每个文章添加阅读时长属性
    for post in post_list:
        # 计算字数（无内容则为0）
        content_length = len(post.content) if post.content else 0
        # 阅读时长：向上取整，每分钟300字
        post.read_time = (content_length + 299) // 300  # 整数除法向上取整
    
    # 2. 配置分页：每页显示5篇文章（可自行修改数字）
    paginator = Paginator(post_list, 6)
    
    # 3. 获取当前页码（从URL参数?page=X中获取）
    page = request.GET.get('page')
    
    try:
        # 4. 获取当前页的文章列表
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是数字，默认显示第1页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        posts = paginator.page(paginator.num_pages)
    
    # 5. 把分页后的文章和分页器传给模板
    return render(request, 'blog/phome.html', {
        'posts': posts,  # 当前页的文章列表
        'paginator': paginator  # 分页器对象（用于模板显示页码）
    })

def archive(request):
    return render(request, "blog/archive.html")

def links(request):
    return render(request, "blog/links.html")

def message(request):
    return render(request, "blog/message.html")

def about(request):
    return render(request, "blog/about.html")

# Create your views here.
