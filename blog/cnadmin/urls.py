# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 22:05
# @Author  : 杨万
# @Email   : 918813641@qq.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from cnadmin import views

urlpatterns=[
    url(r'^$',views.king_index,name='table_index'),
    url(r'^(\w+)/(\w+)/$',views.display_table_obj,name='table_obj'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_obj_change,name='table_obj_change'),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$',views.table_obj_delete,name='table_obj_delete'),
    url(r'^(\w+)/(\w+)/add/$',views.table_obj_add,name='table_obj_add'),
]

