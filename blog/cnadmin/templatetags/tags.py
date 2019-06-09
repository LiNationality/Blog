# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 22:05
# @Author  : 杨万
# @Email   : 918813641@qq.com
# @File    : urls.py
# @Software: PyCharm

from django import template
from django.core.exceptions import *
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta


register=template.Library()

@register.simple_tag
def get_action_verbose_name(admin_class,action):

    action_func = getattr(admin_class, action)
    return action_func.display_name if hasattr(action_func, 'display_name') else action

@register.simple_tag
def render_app_name(admin_class):
    """
       @todo:前端不能使用model_name.model._meta故而巧妙应用自定义标签
       :param model_name:
       :return:
       """
    return admin_class.model._meta.verbose_name

@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_condtions):
    """
    todo:返回标签Filter
    :param filter_field:
    :param admin_class:
    :param filter_condtions:
    :return:
    """
    # select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %filter_field
    select_ele = '''<select class="form-control" name='{filter_field}' ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            print("choice", choice_item, filter_condtions.get(filter_field), type(filter_condtions.get(filter_field)))
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected = ''
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])

        filter_field_name = "%s__gte" % filter_field

    else:
        filter_field_name = filter_field
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)

    return mark_safe(select_ele)

@register.simple_tag
def get_model_name(model_name):
    """
    @todo:前端不能使用model_name.model._meta故而巧妙应用自定义标签
    @todo:作用：间接返回一个前端能用的表名
    :param model_name:
    :return:
    """
    modelname=model_name.model._meta.verbose_name
    return modelname

@register.simple_tag
def get_query_sets(admin_class):

    return admin_class.model.objects.all()

@register.simple_tag
def build_table_header_column(column,orderby_key,filter_condtions,admin_class):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k, v)

    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
        {sort_icon}
        </th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''

        if orderby_key.strip("-") == column:  # 排序的就是这个字段
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''

    else:  # 没有排序
        orderby_key = column
        sort_icon = ''
    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name.upper()
    except FieldDoesNotExist  as e:
        column_verbose_name = getattr(admin_class, column).display_name.upper()
        ele = '''<th><a href="javascript:void(0);">{column}</a></th>'''.format(column=column_verbose_name)
        return mark_safe(ele)

    ele = ele.format(orderby_key=orderby_key, column=column_verbose_name, sort_icon=sort_icon, filters=filters)
    return mark_safe(ele)

@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele=''
    for index,column in enumerate(admin_class.list_display):
        # print(column)
        try:
            field_obj=obj._meta.get_field(column)
            if field_obj.choices:
                column_data=getattr(obj,"get_%s_display"%column)()
            else:
                column_data=getattr(obj,column)
            if type(column_data).__name__=='datetime':
                column_data=column_data.strftime("%Y-%m-%d %H:%M:%S")
            if index==0:
                column_data="<a href='{request_path}{obj_id}/change/'>{data}</a>".format(
                    request_path=request.path,
                    obj_id=obj.nid,
                    data=column_data
                )
        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func=getattr(admin_class,column)
                admin_class.instance=obj
                admin_class.request=request
                column_data=column_func

        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)

@register.simple_tag
def build_paginator(query_sets,filter_condtions,previous_orderby,search_text):
    """
    @todo：返回分页元素
    :param query_sets:
    :param filter_condtions:
    :param previous_orderby:
    :param search_text:
    :return:
    """
    page_btn=''
    filters=''
    for k,v in filter_condtions.items():
        filters+="&%s=%s" % (k,v)

    added_dont_ele=False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages - 2 \
            or abs(query_sets.number-page_num) <= 2:
            """
            @todo: 最前和最后两页
            """
            ele_class=""
            if query_sets.number==page_num:
                added_dont_ele=False
                ele_class="active"
            page_btn+='''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>''' \
                % (ele_class,page_num,filters,previous_orderby,search_text,page_num)

        else:
            """
            @todo:显示省略号
            """
            if added_dont_ele==False:
                page_btn+='<li><a>...</a></li>'
                added_dont_ele=True
    return mark_safe(page_btn)


@register.simple_tag
def get_m2m_obj_list(admin_class,field):

    field_obj=getattr(admin_class.model,field.name)
    return field_obj.rel.to.objects.all()


def recursive_related_objs_lookup(objs,model_name):
    model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        # li_ele = '''<li>
        #     <a href="/configure/web_hosts/change/%s/" >%s</a> </li>''' % (obj.id,obj.__repr__().strip("<>"))
        # ul_ele += li_ele
        # print("-----li",li_ele)
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele +=li_ele
        for related_obj in obj._meta.related_objects:
            if 'ManyToOneRel' not in related_obj.__repr__():
                continue
            if hasattr(obj,related_obj.get_accessor_name()):
                accessor_obj = getattr(obj,related_obj.get_accessor_name())

                if hasattr(accessor_obj,'select_related'):
                    target_objs = accessor_obj.select_related() #.filter(**filter_coditions)

                else:
                    #print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj
                if len(target_objs) >0:
                    #print("\033[31;1mdeeper layer lookup -------\033[0m")
                    nodes = recursive_related_objs_lookup(target_objs,model_name)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele

@register.simple_tag
def display_obj_related(objs):
    """
    todo:取出所有关联数据
    :param obj:
    :return:
    """
    if objs:
        # model_class=objs[0]._meta.model
        model_class=objs[0]._meta.model

        model_name=objs[0]._meta.model_name
        """测试开始"""
        # print(model_class,model_name)
        """结束测试"""
        return mark_safe(recursive_related_objs_lookup(objs,model_name))


# @register.simple_tag
# def get_m2m_obj_list(admin_class,field,form_obj):
#     '''返回m2m所有待选数据'''
#     # 表结构对象的某个字段
#     field_obj = getattr(admin_class.model, field.name)
#     all_obj_list = field_obj.rel.to.objects.all()
#
#     # 单条数据的对象中的某个字段
#     if form_obj.instance.nid:
#         obj_instance_field = getattr(form_obj.instance, field.name)
#         selected_obj_list = obj_instance_field.all()
#     else:  # 代表这是在创建新的一条记录
#         return all_obj_list
#         pass
#
#     standby_obj_list = []
#     for obj in all_obj_list:
#         if obj not in selected_obj_list:
#             standby_obj_list.append(obj)
#
#     return standby_obj_list
#
# @register.simple_tag
# def get_m2m_selected_obj_list(form_obj,field):
#     '''返回已选择的m2m数据'''
#     if form_obj.instance.id :
#         field_obj = getattr(form_obj.instance,field.name)
#         return field_obj.all()
