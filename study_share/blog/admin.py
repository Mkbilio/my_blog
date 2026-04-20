from django.contrib import admin
from .models import Post

# 注册文章模型到后台
admin.site.register(Post)