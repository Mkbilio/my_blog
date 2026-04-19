from django.urls import path
from . import views
urlpatterns = [
    path("",views.blog_home,name="blog_home"),
    path("post/<int:pk>/",views.post_detail,name="post_detail"),
    path("post/create/",views.post_create,name="post_create"),
    path("category/<int:cate_id>/",views.post_by_category,name="post_vy_category"),
    #以下是页面上导航
    path("phome/",views.phome,name="phome"),
    path("archive/",views.archive,name="archive"),
    path("links/",views.links,name="links"),
    path("message/",views.message,name="message"),
    path("about/",views.about,name="about"),
]

