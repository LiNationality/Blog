from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像',null=True,blank=True)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,null=True)

    fans = models.ManyToManyField(verbose_name='粉丝们', to='UserInfo', through='UserFans',
                                  through_fields=('user', 'follower'),blank=True,null=True)



    def __str__(self):
        return self.username
    class Meta:
        verbose_name='用户表'
        verbose_name_plural='用户表'



class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid',verbose_name='用户',on_delete=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='博客信息表'
        verbose_name='博客信息表'


class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users',on_delete=True)
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers',on_delete=True)

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]
        verbose_name='互粉关系表'
        verbose_name_plural = '互粉关系表'


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=True)
    class Meta:
        verbose_name = '博主个人文章分类表'
        verbose_name_plural='博主个人文章分类表'
    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid',on_delete=True)
    class Meta:
        verbose_name_plural='文章详细表'
        verbose_name='文章详细表'

class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid',on_delete=True)
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid',on_delete=True)
    up = models.BooleanField(verbose_name='是否赞')
    def __str__(self):
        return '点赞表'
    class Meta:
        unique_together = [
            ('article', 'user'),
        ]
        verbose_name_plural = '文章顶或踩表'
        verbose_name  = '文章顶或踩表'


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True,on_delete=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid',on_delete=True)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid',on_delete=True)
    class Meta:
        verbose_name_plural='评论表'
        verbose_name='评论表'


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=True)
    class Meta:
        verbose_name_plural='标签表'
        verbose_name='标签表'


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0,verbose_name='阅读量')
    comment_count = models.IntegerField(default=0,verbose_name='评论量')
    up_count = models.IntegerField(default=0,verbose_name='点赞量')
    down_count = models.IntegerField(default=0,verbose_name='被踩量')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=True)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True,on_delete=True)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]

    article_type = models.IntegerField(choices=type_choices, default=None,verbose_name='所属类型')

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='文章表'
        verbose_name='文章表'


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid',on_delete=True)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid',on_delete=True)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

        verbose_name_plural = '文章与标签'
        verbose_name = '文章与标签'
