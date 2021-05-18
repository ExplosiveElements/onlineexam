
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from student import views

urlpatterns = [
    #管理员登陆
    path('admin/', admin.site.urls),
    #前往学生/老师说明
    url(r'^toDescription/',views.toDescription),
    #学生登陆
    url(r'^toStudent/',views.toStudent),
    url(r'^studentLogin/',views.studentLogin),
    url(r'^studentActions/',views.studentActions),
    #教师登陆
    url(r'^toTeacher/',views.toTeacher),
    url(r'^teacherLogin/',views.teacherLogin),
    url(r'^teacherActions/', views.teacherActions),
    #默认访问首页
    url(r'^$',views.index),
    # 前往首页
    url(r'^toIndex',views.toIndex),
    #前往某一个试卷分析
    url('showGrade',views.showGrade),
    url('papergradesget', views.papergradesget),
    # 根据教师获取学生成绩
    url('queryStudent',views.queryStudent),
    # 前往学生考试
    url(r'^startExam',views.startExam),
    # 计算学生考试成绩
    url(r'^calGrade',views.calGrade),
    # 学生获取自己的成绩
    url(r'^stugradesget', views.stugradesget),
    # 学生获取自己要参加的考试信息
url(r'^stugetPapers', views.stugetPapers),
    # 退出登录
    url(r'^logout/$',views.logOut),
    #题库管理
        # 数据获取
    url(r'^getAbilitys',views.getAbilitys),
   url(r'^questionDataGet',views.questionDataGet),
    url(r'^fillQuestionDataGet',views.fillQuestionDataGet),
        # 能力评级管理
    url(r'^abilityadd',views.abilityadd),
    url(r'^abilityshow', views.abilityshow),
    url(r'^abilitydel', views.abilitydel),
        # 题目管理
    url(r'^questionadd', views.questionadd),
    url(r'^filladd', views.filladd),
url(r'^questionsdel', views.questionsdel),
url(r'^fillquestionsdel', views.fillquestionsdel),
url(r'^questionedit', views.questionedit),
url(r'^filledit', views.filledit),
# 试卷管理
    # 试卷信息获取
url(r'^getPapers', views.getPapers),
    # 组卷
url(r'^type_number', views.type_number),
url(r'^ability_numbers', views.ability_numbers),
url(r'^subject_number_get', views.subject_number_get),
    # 试卷管理
url(r'^paperadd', views.paperadd),
url(r'^paperdel', views.paperdel),
url(r'^papershow', views.papershow),
    # 获取成绩画图数据
url(r'^subjectshow', views.subjectshow),
url(r'^studentssubjectshow', views.studentssubjectshow),
]
