from cnblog import models
from django.shortcuts import redirect,render,HttpResponse

enabled_admins={}

class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []
    readonly_fields = []
    # actions = ["delete_selected_objs", ]
    readonly_table = False
    modelform_exclude_fields = []
    pass

class UserInfoAdmin(BaseAdmin):
    list_display = [ 'nid','email','username','nickname','avatar',]
    list_per_page = 5
    # list_filters = ['username','nickname','email','avatar',]
    search_fields = ['username','nickname','email',]
    filter_horizontal=['fans',]
    def test(self, request, querysets):
        print("in test", )

    test.display_name = "测试动作"

    # def default_form_validation(self):
    #     #print("-----customer validation ",self)
    #     #print("----instance:",self.instance)
    #
    #     consult_content =self.cleaned_data.get("content",'')
    #     if len(consult_content) <15:
    #         return self.ValidationError(
    #                         ('Field %(field)s 咨询内容记录不能少于15个字符'),
    #                         code='invalid',
    #                         params={'field': "content",},
    #                    )



def register(model_class,admin_class):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label]={}

    # admin_class.obj=admin_class()
    admin_class.model=model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name]=admin_class
    # enabled_admins['crmadmin']['customerfollowup']=CustomerFollowUpAdmin
    pass



class Useradmin(BaseAdmin):
    list_display = ['']


class BogAdmin(BaseAdmin):

    list_display = ['nid','user','title','site']


register(models.UserInfo,UserInfoAdmin)
register(models.Blog,BaseAdmin)




