from django.contrib import admin
from student.models import *
# 修改名称
admin.site.site_header = '在线考试系统后台'
admin.site.site_title = '在线考试系统'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name','sex','dept','major','password','email','birth')# 要显示哪些信息
    list_display_links = ('id','name')#点击哪些信息可以进入编辑页面
    search_fields = ['name','dept','major','birth']   #指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
    list_filter =['name','dept','major','birth']#指定列表过滤器，右边将会出现一个快捷的过滤选项


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'dept', 'password', 'email', 'birth')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'dept', 'birth']
    list_filter = ['name','dept']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','tea_id','subject')
    list_display_links = ('id','tea_id','subject')


@admin.register(Dept)
class DeptAdmin(admin.ModelAdmin):
    list_display = ('id','dept')
    list_display_links = ('id','dept')


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('id','major','dept')
    list_display_links = ('id','major','dept')
