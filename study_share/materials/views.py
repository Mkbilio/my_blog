from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Material,Category
from django import forms
from materials.models import Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # Django自带注册表单
from django.contrib import messages  # 提示信息
from django.contrib.auth.decorators import login_required
from .models import Notice, NoticeComment
from .forms import NoticeForm, NoticeCommentForm
# 定义一个函数：处理首页请求
def index(request):
    # 返回文字给浏览器
    return render(request, "index.html")
def hello(request):
    return HttpResponse("Hello world")
class MaterialForm(forms.ModelForm):
    class Meta:
        #model是django的关键字，告诉表单 绑定哪一个数据库表！
        model = Material
        fields = ['title','category','file']
def upload_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("上传成功！<a href='/upload/'>继续上传</a>")
    else:
        form = MaterialForm()
    return render(request, "upload.html",{"form":form})
# 展示所有资料
def material_list(request):
    # 1. 获取所有分类（用于页面显示按钮）
    from materials.models import Category  # 导入分类模型
    categories = Category.objects.all()
    # 2. 获取用户点击的分类 ID
    category_id = request.GET.get('category', '')
    # 3. 获取用户搜索的关键词（保留之前的搜索功能）
    keyword = request.GET.get('keyword', '')
    # 4. 初始：所有资料
    materials = Material.objects.all()
    # 5. 如果选了分类，就按分类筛选
    if category_id:
        materials = materials.filter(category_id=category_id)
    # 6. 如果有搜索词，再按标题搜索（可以和分类同时用）
    if keyword:
        materials = materials.filter(title__icontains=keyword)
    # 7. 把数据传给页面
    return render(request, 'material_list.html', {
        'materials': materials,
        'categories': categories,
        'current_category_id': category_id,  # 当前选中的分类 ID
        'keyword': keyword
    })
@login_required  # 👈 加这一行！必须登录才能访问
def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'upload.html', {'form': form})
def register(request):
    # 如果是POST请求（提交注册信息）
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 保存新用户
            username = form.cleaned_data.get('username')
            messages.success(request, f'用户 {username} 注册成功！请登录')
            return redirect('login')  # 跳登录页
    # 如果是GET请求（访问注册页）
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# ========== 1. 通知列表页（所有人可见，仅展示） ==========
def notice_list(request):
    # 只显示「启用且未删除」的通知
    notices = Notice.objects.filter(is_active=True)
    # 判断是否是管理员（staff=True 是Django管理员标识）
    context = {
        "notices": notices,
        "is_admin": request.user.is_authenticated and request.user.is_staff,
    }
    return render(request, "notice/list.html", context)

# ========== 2. 通知详情页（用户可评论，仅展示） ==========
def notice_detail(request, notice_id):
    # 获取通知（不存在则404，仅显示启用的）
    notice = get_object_or_404(Notice, id=notice_id, is_active=True)
    # 获取该通知的「未删除」评论
    comments = notice.comments.filter(is_deleted=False)
    # 初始化评论表单
    comment_form = NoticeCommentForm()

    # 处理评论提交（仅登录用户可提交）
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = NoticeCommentForm(request.POST)
        if comment_form.is_valid():
            # 先不保存，补充关联字段
            comment = comment_form.save(commit=False)
            comment.notice = notice  # 关联当前通知
            comment.user = request.user  # 关联当前登录用户
            comment.save()  # 最终保存
            messages.success(request, "评论提交成功！")
            return redirect("notice_detail", notice_id=notice.id)  # 刷新页面避免重复提交

    context = {
        "notice": notice,
        "comments": comments,
        "comment_form": comment_form,
        "is_admin": request.user.is_authenticated and request.user.is_staff,
    }
    return render(request, "notice/detail.html", context)

# ========== 3. 发布通知（仅管理员可访问） ==========
@login_required  # 必须登录
def notice_create(request):
    # 核心权限：非管理员直接拒绝
    if not request.user.is_staff:
        messages.error(request, "只有管理员才能发布通知！")
        return redirect("notice_list")
    
    # 处理表单提交
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user  # 强制赋值为当前管理员
            notice.save()
            messages.success(request, "通知发布成功！")
            return redirect("notice_list")
    else:
        form = NoticeForm()  # 初始化空表单

    context = {"form": form, "title": "发布新通知"}
    return render(request, "notice/form.html", context)

# ========== 4. 编辑通知（仅管理员可访问） ==========
@login_required
def notice_edit(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    # 非管理员拒绝访问
    if not request.user.is_staff:
        messages.error(request, "只有管理员才能编辑通知！")
        return redirect("notice_list")
    
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "通知编辑成功！")
            return redirect("notice_detail", notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)  # 填充已有数据

    context = {"form": form, "title": "编辑通知", "notice": notice}
    return render(request, "notice/form.html", context)

# ========== 5. 删除通知（仅管理员可访问） ==========
@login_required
def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    # 非管理员拒绝访问
    if not request.user.is_staff:
        messages.error(request, "只有管理员才能删除通知！")
        return redirect("notice_list")
    
    notice.delete()  # 物理删除（也可改为 notice.is_active=False 隐藏）
    messages.success(request, "通知删除成功！")
    return redirect("notice_list")

# ========== 6. 删除评论（用户删自己的，管理员删所有） ==========
@login_required
def comment_delete(request, comment_id):
    # 获取未删除的评论
    comment = get_object_or_404(NoticeComment, id=comment_id, is_deleted=False)
    notice_id = comment.notice.id  # 保存通知ID，删除后返回详情页

    # 权限判断：① 管理员 或 ② 评论作者本人
    if not (request.user.is_staff or request.user == comment.user):
        messages.error(request, "你没有权限删除这条评论！")
        return redirect("notice_detail", notice_id=notice_id)
    
    # 软删除：标记为已删除（而非删除数据）
    comment.is_deleted = True
    comment.save()
    messages.success(request, "评论删除成功！")
    return redirect("notice_detail", notice_id=notice_id)
# Create your views here.
