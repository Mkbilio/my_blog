from django import forms
from .models import Notice, NoticeComment

# 1. 通知编辑表单（仅管理员用）
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "content", "is_active"]  # 管理员可编辑的字段（不含created_by，视图自动赋值）
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "输入通知标题"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10, "placeholder": "输入通知详情"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "通知标题",
            "content": "通知内容",
            "is_active": "是否在前台显示",
        }

# 2. 评论提交表单（仅用户用）
class NoticeCommentForm(forms.ModelForm):
    class Meta:
        model = NoticeComment
        fields = ["content"]  # 仅需输入评论内容
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "请输入你的评论（文明发言）"}),
        }
        labels = {
            "content": "",  # 隐藏标签，更美观
        }