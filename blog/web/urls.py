# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 22:05
# @Author  : 杨万
# @Email   : 918813641@qq.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from web import views
urlpatterns=[
    url(r'^$',views.index,name='sales_index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^check_code.html$', views.check_code,name='check_code'),
]

