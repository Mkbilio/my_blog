"""
URL configuration for study_share project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from materials import views  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
# 新增代码2：绑定「空网址」和「index函数」→ 访问首页时执行index函数
    path('', views.index,name="index"), 
    path("blog/",include("blog.urls")),
    path('hello',views.hello,name="hello"),
    path('upload/',views.upload_material,name='upload'),    # 👈 上传页面
    path('list/',views.material_list,name='material_list'),
    # 登录/注销/注册路由
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='index',
        http_method_names=['get', 'post']
    ), name='logout'),
    path('register/', views.register, name='register'), # 新增注册路由
    # ========== 新增：通知+评论路由 ==========
    path('notices/', views.notice_list, name='notice_list'),  # 通知列表
    path('notices/<int:notice_id>/', views.notice_detail, name='notice_detail'),  # 通知详情
    path('notices/create/', views.notice_create, name='notice_create'),  # 发布通知（仅管理员）
    path('notices/<int:notice_id>/edit/', views.notice_edit, name='notice_edit'),  # 编辑通知（仅管理员）
    path('notices/<int:notice_id>/delete/', views.notice_delete, name='notice_delete'),  # 删除通知（仅管理员）
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'), # 删除评论
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 保留媒体文件路由
# 👇 关键：添加媒体文件的访问规则（仅在开发模式下生效）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)