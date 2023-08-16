from django.contrib import admin
from blog.models import *
from django_jalali.admin.filters import JDateFieldListFilter

admin.sites.AdminSite.site_header = 'پنل مدیریت جنگو'
admin.sites.AdminSite.site_title = 'پنل مدیریت جنگو'
admin.sites.AdminSite.index_title = 'پنل مدیریت جنگو'


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


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
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject']
    search_fields = ['name', 'subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter)]
    search_fields = ['name', 'body']
    raw_id_fields = ['post']
    ordering = ['name', 'created']
    list_editable = ['active']
    list_display_links = ['post', 'name']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']
    list_filter = [('created', JDateFieldListFilter)]
    search_fields = ['title', 'description']
    raw_id_fields = ['post']
