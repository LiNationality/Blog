from django.shortcuts import render,HttpResponse,redirect
from cnadmin import cnadmin
from cnadmin.utils import page_utils,Form_model

"""
@todo:获取django自带分页功能
"""
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from cnblog.models import *
# Create your views here.



def king_index(request):
    # print("cnadmin的views中",cnadmin.enabled_admins)
    return render(request,'king_admin_tmp/table_index.html',
                  {'table_list':cnadmin.enabled_admins,
                    'request':request,
                   })
    pass

def table_obj_add(request,app_name,table_name):
    """
    todo:添加页
    :param request:
    :param app_name:
    :param table_name:
    :param obj_id:
    :return:
    """
    # print('Add页面')
    admin_class = cnadmin.enabled_admins[app_name][table_name]
    model_form_class = Form_model.create_model_form(request, admin_class)

    # obj = admin_class.model.objects.get(nid=obj_id)
    if request.method == "POST":
        # print("cnadmin中的table_obj_change的POST参数",request.POST)
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()

            return redirect(request.path.replace('/add/','/'))
    else:
        form_obj = model_form_class()

    """测试代码"""
    # print(admin_class.filter_horizontal)
    # for field in form_obj:
    # print(field.name)
    # field_obj = getattr(admin_class.model, field.name).objects
    # print(field_obj)
    # all_obj_list = field_obj
    """测试结束"""
    # form_obj=model_form_class()
    return render(request,'king_admin_tmp/table_obj_add.html',{
        'form_obj':form_obj,
        'admin_class':admin_class,
    })

def table_obj_change(request,app_name,table_name,obj_id):
    """
    todo:修改页
    :param request:
    :param app_name:
    :param table_name:
    :param obj_id:
    :return:
    """
    print('修改函数',request.path)
    admin_class=cnadmin.enabled_admins[app_name][table_name]
    model_form_class=Form_model.create_model_form(request,admin_class)

    obj=admin_class.model.objects.get(nid=obj_id)
    if request.method=="POST":
        # print("cnadmin中的table_obj_change的POST参数",request.POST)
        form_obj=model_form_class(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
    else:
        form_obj=model_form_class(instance=obj)

    """测试代码"""
    # print(admin_class.filter_horizontal)
    # for field in form_obj:
        # print(field.name)
        # field_obj = getattr(admin_class.model, field.name).objects
        # print(field_obj)
        # all_obj_list = field_obj

    """测试结束"""

    return render(request,"king_admin_tmp/table_obj_change.html",
                  {
                    'form_obj':form_obj,
                    "admin_class":admin_class,
                    "app_name":app_name,
                    "table_name":table_name
                  })

def display_table_obj(request,app_name,table_name):
    """
    todo：显示app表格
    :param request:
    :param app_name:
    :param table_name:
    :return:
    """
    # for i in range(100):
    #     obj=UserInfo.objects.create(username=str(int('20191101000')+i),password='123456',nickname='stu-'+str(i),email=str(int('20191101000')+i)+'@stu.com')
    #     obj.save()
    # print("cnadmin中的view中的display_table_obj的接收参数:",app_name,table_name)
    admin_class=cnadmin.enabled_admins[app_name][table_name]

    if request.method == "POST":  # action 来了

        # print(request.POST)
        selected_ids = request.POST.get("selected_ids")
        action = request.POST.get("action")
        if selected_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(','))
        else:
            raise KeyError("No object selected.")
        if hasattr(admin_class, action):
            action_func = getattr(admin_class, action)
            request._admin_action = action
            return action_func(admin_class, request, selected_objs)


    object_list,filter_condtions=page_utils.table_filter(request,admin_class)
    object_list=page_utils.table_search(request,admin_class,object_list)
    object_list,orderby_key=page_utils.table_short(request,admin_class,object_list)
    print('cnadmin的views的display_table_obj的orderby_key',orderby_key)
    paginator=Paginator(object_list,admin_class.list_per_page)

    page=request.GET.get('page')
    try:
        query_sets=paginator.page(page)
    except PageNotAnInteger:
        query_sets=paginator.page(1)
    print(query_sets.has_previous)
    return render(request, 'king_admin_tmp/table_obj.html',
                  {
                    'admin_class':admin_class,
                    'query_sets':query_sets,
                    'filter_condtions':filter_condtions,
                    'orderby_key':orderby_key,
                  })
    pass

def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = cnadmin.enabled_admins[app_name][table_name]
    obj=admin_class.model.objects.get(nid=obj_id)


    print("Delete函数的obj",type(obj))
    print("Delete函数的obj",obj)


    if request.method=='POST':
        obj.delete()
        return redirect("/cnadmin/%s/%s" % (app_name,table_name))



    return render(request,'king_admin_tmp/table_obj_delete.html',
    {
        'obj':obj,
        'admin_class':admin_class,
        'app_name':app_name,
        'table_name':table_name,
    })