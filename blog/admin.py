from django.contrib import admin
from blog.models import *
from django_jalali.admin.filters import JDateFieldListFilter


admin.sites.AdminSite.site_header = 'پنل مدیریت جنگو'
admin.sites.AdminSite.site_title = 'پنل مدیریت جنگو'
admin.sites.AdminSite.index_title = 'پنل مدیریت جنگو'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'publish', 'status']
    ordering = ['title', 'publish']
    list_filter = [('publish', JDateFieldListFilter), 'status', 'author']
    search_fields = ['title', 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    list_display_links = ['author', 'title']
