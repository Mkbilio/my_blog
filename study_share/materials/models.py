# 保留原生导入（渲染HTML用）
from django.db import models
# 导入Django的数据库模型工具（核心！用来建表）
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

class Category(models.Model):
     # 字段1：分类名称（字符串，最大长度100，不允许为空）
    name = models.CharField("分类名称",max_length=100,null=False,blank=False)
    # 字段2：创建时间（自动记录，不用手动填）
    create_time = models.DateTimeField("创建时间",auto_now_add=True)
    def  __str__(self):
        return self.name
    class Meta:
        verbose_name = "资料分类"
        verbose_name_plural = "资料分类"
class Material(models.Model):
    # 字段1:资料标题
    title = models.CharField("资料标题",max_length=200,null=False,blank=False)
    # 字段2：关联分类（和Category表关联，删除分类时同步删除资料）
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="所属分类")
    # 字段3：资料文件（上传文件用
    file = models.FileField("资料文件",upload_to="materials/")
     # 字段4：上传时间
    upload_time = models.DateTimeField("上传时间", auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "复习资料"
        verbose_name_plural = "复习资料"
class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="通知标题")  # 通知标题
    content = models.TextField(verbose_name="通知内容")  # 通知详情
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="notices", 
        verbose_name="发布管理员"
    )  # 关联发布的管理员
    created_at = models.DateTimeField(default=timezone.now, verbose_name="发布时间")  # 发布时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")  # 自动更新修改时间
    is_active = models.BooleanField(default=True, verbose_name="是否显示")  # 是否在前台展示

    class Meta:
        verbose_name = "网站通知"
        verbose_name_plural = "网站通知"
        ordering = ["-created_at"]  # 最新通知排在最前

    def __str__(self):
        return self.title  # 后台显示通知标题

# 新增：通知评论模型（用户可评论、删自己的，管理员删所有）
class NoticeComment(models.Model):
    notice = models.ForeignKey(
        Notice, 
        on_delete=models.CASCADE, 
        related_name="comments", 
        verbose_name="所属通知"
    )  # 关联对应的通知
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="notice_comments", 
        verbose_name="评论用户"
    )  # 关联评论的用户
    content = models.TextField(verbose_name="评论内容")  # 评论详情
    created_at = models.DateTimeField(default=timezone.now, verbose_name="评论时间")  # 评论时间
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")  # 软删除（避免误删）

    class Meta:
        verbose_name = "通知评论"
        verbose_name_plural = "通知评论"
        ordering = ["created_at"]  # 最早评论排在最前

    def __str__(self):
        return f"{self.user.username} 评论：{self.content[:20]}"  # 后台简短显示评论

    
