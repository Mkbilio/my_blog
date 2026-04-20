from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('文章标题',max_length=200)
    content = models.TextField("文章正文")
    category = models.CharField('文章分类',max_length=200,default='日常')
    publish_time = models.DateTimeField('发布时间', default=timezone.now)
    views = models.IntegerField('阅读量', default=0)
    excerpt = models.TextField('文章摘要', blank=True, null=True)
    photo = models.ImageField(("文章封面图"), upload_to='post_images', blank=True,null=True)
    def __str__(self):
        return self.title
    # 中文表名
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'