from django.contrib import admin
from .models import Category,Material
from .models import Notice,NoticeComment

admin.site.register(Category)
admin.site.register(Material)
# 用装饰器注册，简洁清晰
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at",)

# 通知评论模型注册（修复字段名 + 优化显示）
@admin.register(NoticeComment)
class NoticeCommentAdmin(admin.ModelAdmin):
    # 1. 修复：把 commenter 改成模型里实际的字段名 user
    # 2. 优化：新增 get_username 方法，显示用户名而非 User object (1)
    list_display = ("notice", "get_username", "content", "created_at", "is_deleted")
    search_fields = ("content", "user__username")  # 支持按用户名搜索
    list_filter = ("created_at", "notice", "is_deleted")
    list_editable = ("is_deleted",)  # 可直接在列表页修改是否删除

    # 自定义方法：显示用户的用户名（核心优化）
    def get_username(self, obj):
        return obj.user.username  # 从 user 外键中提取用户名
    # 给自定义字段加中文显示名
    get_username.short_description = "评论用户"

    # 可选：只显示未删除的评论（默认），后台可手动筛选已删除的
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)
# Register your models here.
