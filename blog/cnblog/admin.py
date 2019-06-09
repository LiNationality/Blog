from django.contrib import admin

# Register your models here.
from cnblog.models import *
# Register your models here.
class userInfo(admin.ModelAdmin):
    list_display = (
        'nid','username','nickname','email','avatar',
    )
    list_per_page = 10
    search_fields = ('username',)

admin.site.register(UserInfo,userInfo)
# admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(UserFans)
admin.site.register(Category)
admin.site.register(ArticleDetail)
admin.site.register(UpDown)
admin.site.register(Comment)
admin.site.register(Article)
admin.site.register(Article2Tag)