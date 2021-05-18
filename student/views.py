from django.views.decorators.http import require_POST
from django.db.models import Q
from django.shortcuts import render,redirect
from student import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
import random
import time
import json

# Create your views here.

from django.template.defaulttags import register
# 为模板添加类似python range函数的内容
@register.filter
def get_range(value):
    return range(value)


# 用于组装列表
def assembly(sample):
    components= []
    for i in range(0,len(sample)):
        tempt = str(sample[i][0])
        components.append(tempt)
    return components


# 获取学生端课程列表
def studentsubjectlistget(student):
    subject_list = []
    grades = models.Grade.objects.filter(sid=student)
    for grade in grades:
        subject_list.append(grade.subject)
    subject_list = list(set(subject_list))
    return subject_list


# 前往首页
def index(request):
    return render(request,'index.html')

# 前往首页
def toIndex(request):
    return render(request,'index.html')

# 退出登录
def logOut(request):
    return redirect('/toIndex/')

# 前往师生说明页
def toDescription(request):
    return render(request,'studentDescription.html')

# 学生登陆视图函数
# 前往学生登录页面
def toStudent(request):
    return render(request, 'studentlogin.html')



# 学生登录
@require_POST
def studentLogin(request):
    if request.method=='POST':
        #print(1)
        # 获取表单信息
        stuId=request.POST.get('stuid')
        password=request.POST.get('password')
        # print("stuid",stuId,"password",password)
        # 通过学号获取该学生实体
        try:
            student=models.Student.objects.get(id=stuId)
        except ObjectDoesNotExist:
            return render(request,'studentlogin.html',{'message':'您输入的学号不存在'})
        else:
            #print(student)
            if password==student.password:  #登录成功
                if student.email :

                    subject_list = studentsubjectlistget(student)
                    return render(request, 'student.html', {'student': student,'flag':'3','subjects':json.dumps(subject_list)})
                else:

                    return render(request, 'studentactive.html', {'student': student})
            else:
                return render(request,'studentlogin.html',{'msg':'密码不正确'})

@require_POST
# 学生激活 视图函数
def studentActions(request):
    if request.method == 'POST':
        stuid_flag = request.POST.get('stuid_flag')
        stuid_flag_list = stuid_flag.split("-")
        stuid=stuid_flag_list[0]
        flag = stuid_flag_list[1]
        student = models.Student.objects.get(id=stuid)
        sex = request.POST.get('sex')
        passwords = request.POST.get('password')
        email = request.POST.get('email')
        birth = request.POST.get('birth')
        student.sex = sex
        student.password = passwords
        student.birth = birth
        student.email = email
        student.save()
        subject_list = studentsubjectlistget(student)
        # 查询成绩信息
        return render(request,'student.html', {'student': student, 'flag':flag,'subjects':json.dumps(subject_list)})



# 教师登陆 视图函数
# 前往教师登录页面
def toTeacher(request):
    return render(request,'teacherlogin.html')
# 教师登录
def teacherLogin(request):

    if request.method == 'POST':
        teaId = request.POST.get('teaid')
        password = request.POST.get('password')
        flag = request.POST.get('flag')
        # print("id", teaId, "password", password)
        if flag ==None:
            flag = '3'
        try:
            teacher=models.Teacher.objects.get(id=teaId)
        except ObjectDoesNotExist:
            return render(request, 'teacherlogin.html', {'message': '您输入的教师工号不存在'})
        else:
            #print(teacher)
            if password == teacher.password:  # 登录成功
                if teacher.email:
                    subjectlist = []
                    papers = models.Paper.objects.filter(tid_id=teaId)
                    for paper in papers:
                        subjectlist.append(paper.subject)
                    subjectlist = list(set(subjectlist))
                    return render(request, 'teacher.html', {'teacher': teacher,'falg':flag,'subjects':json.dumps(subjectlist)})
                else:
                    return render(request, 'teacheractive.html', {'teacher': teacher})

            else:
                return render(request, 'teacherlogin.html', {'msg': '密码不正确'})
# 教师激活视图函数
def teacherActions(request):
    if request.method == 'POST':
        teaid_flag = request.POST.get('teaid_flag')
        teaid_flag_list = teaid_flag.split("-")
        teaid = teaid_flag_list[0]
        flag = teaid_flag_list[1]
        teacher = models.Teacher.objects.get(id=teaid)
        sex = request.POST.get('sex')
        passwords = request.POST.get('password')
        email = request.POST.get('email')
        birth = request.POST.get('birth')
        teacher.sex = sex
        teacher.password = passwords
        teacher.birth = birth
        teacher.email = email
        teacher.save()
        subjectlist = []
        subjects = models.Subject.objects.filter(tea_id_id=teaid)
        for subject in subjects:
            subjectlist.append(subject.subject)
        return render(request, 'teacher.html', {'teacher': teacher,  'falg':flag,'subject':json.dumps(subjectlist) })

#教师查看成绩
def showGrade(request):
    paper_id=request.GET.get('paper_id')
    teacher_id = request.GET.get('tea_id')
    teacher = models.Teacher.objects.get(id=teacher_id)
    paper = models.Paper.objects.get(id=paper_id)
    grades1 = models.Grade.objects.filter(paper=paper)
    grades = []
    for grade in grades1:
        grades.append(grade.grade)
    subject1 = paper.subject
    top = max(grades)
    last = min(grades)
    average = sum(grades)/len(grades)
    data1 = models.Grade.objects.filter(paper=paper, grade__lt=60).count()
    data2 = models.Grade.objects.filter(paper=paper, grade__gte=60, grade__lt=70).count()
    data3 = models.Grade.objects.filter(paper=paper, grade__gte=70, grade__lt=80).count()
    data4 = models.Grade.objects.filter(paper=paper, grade__gte=80, grade__lt=90).count()
    data5 = models.Grade.objects.filter(paper=paper, grade__gte=90).count()

    question_no = []
    question_rate = []
    questions_an = models.QuestionAnswer.objects.filter(pid=paper)
    for x in range(0,questions_an.count()):
        y=x+1
        question_no.append('第'+str(y)+'选择题')
        question_rate.append(questions_an[x].right/questions_an[x].all*100)

    fill_on = []
    fill_rate = []
    fill_an = models.FillQuestionAnswer.objects.filter(pid=paper)
    for x in range(0,fill_an.count()):
        y=x+1
        fill_on.append('第'+str(y)+'填空题')
        fill_rate.append(fill_an[x].right/fill_an[x].all*100)

    ques_ans = {'datax':json.dumps(question_no),'datay':json.dumps(question_rate)}
    fill_ans = {'datax':json.dumps(fill_on),'datay':json.dumps(fill_rate)}
    data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5,'top':top,'last':last,'average':average}

    return render(request,'showGrade.html',{'data':data,'subject':subject1,'teacher':teacher,'paper':paper,'ques_ans':ques_ans,'fill_ans':fill_ans})


# 教师获取对应试卷成绩
def papergradesget(request):
    if request.method == 'GET':
        paperid = request.GET['paperid']
        stuid = request.GET['student_id']
        stu_sex = request.GET['student_sex']
        stu_major = request.GET['student_major']
        paper = models.Paper.objects.get(id=paperid)
        rows = []
        if (stuid == '') and (stu_sex == '')and (stu_major == ''):
            grades = models.Grade.objects.filter(paper=paper)
        elif (stuid != '') and (stu_sex == '')and (stu_major == ''):
            grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid_id=stuid))
        elif (stuid == '') and (stu_sex != '')and (stu_major == ''):
            grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__sex=stu_sex))
        elif (stuid == '') and (stu_sex == '') and (stu_major != ''):
            grades = models.Grade.objects.filter(Q(paper=paper) & Q(sid__major=stu_major))
        elif (stuid != '') and (stu_sex != '') and (stu_major == ''):
            grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__sex=stu_sex)&Q(sid_id=stuid))
        elif (stuid != '') and (stu_sex == '') and (stu_major != ''):
            grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__major=stu_major)&Q(sid_id=stuid))
        elif (stuid == '') and (stu_sex != '') and (stu_major != ''):
            grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__major=stu_major)&Q(sid__sex=stu_sex))
        else:
            grades = models.Grade.objects.filter(Q(paper=paper) & Q(sid__major=stu_major) & Q(sid__sex=stu_sex)&Q(sid_id=stuid))
        total = len(grades)
        for grade in grades :
            rows.append({'stuid': grade.sid.id, 'stuname': grade.sid.name, 'subject': paper.subject,
                             'major': grade.sid.major.major, 'grade': grade.grade})
        data = {"total": total, "rows": rows}
        return JsonResponse(data)


#教师获取学生成绩
def queryStudent(request):
    if request.method == 'GET':
        teaid = request.GET['teacherid']
        stuid = request.GET['student_id']
        stu_sex = request.GET['student_sex']
        paper_name = request.GET['paper_name']
        if paper_name == '':
            papers = models.Paper.objects.filter(tid=teaid)
        else:
            papers = models.Paper.objects.filter(Q(tid=teaid)&Q(name=paper_name))
        rows = []
        total = 0
        for paper in papers:
            if (stuid == '') and (stu_sex == ''):
                grades = models.Grade.objects.filter(paper=paper)
            elif (stuid != '') and (stu_sex == ''):
                grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid_id=stuid))
            elif (stuid == '') and (stu_sex != ''):
                grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__sex=stu_sex))
            else:
                grades = models.Grade.objects.filter(Q(paper=paper)&Q(sid__sex=stu_sex)&Q(sid_id=stuid))
            total += len(grades)
            for grade in grades :
                rows.append({'id': grade.sid.id, 'name': grade.sid.name, 'subject': paper.subject,
                             'major': grade.sid.major.major, 'papername': paper.name, 'grade': grade.grade})
        data = {"total": total, "rows": rows}
        return JsonResponse(data)


# 学生获取自己成绩
def stugradesget(request):
    if request.method == 'GET':
        stuid = request.GET['stuid']
        grades = models.Grade.objects.filter(sid_id=stuid)
        rows = []
        total = len(grades)
        for grade in grades:
            rows.append({'id':grade.paper.id,'teacher_name':grade.paper.tid.name,'subject':grade.subject,'papername':grade.paper.name,'grade':grade.grade})
        data = {"total": total, "rows": rows}
        return JsonResponse(data)

#学生考试的视图函数
def startExam(request):
    sid = request.GET.get('sid')
    paper_id=request.GET.get('paper_id')
    student=models.Student.objects.get(id=sid)
    paper=models.Paper.objects.get(id=paper_id)
    count = models.Grade.objects.filter(Q(sid_id=sid)&Q(paper=paper)).count()
    now1 = timezone.now()
    starttime = paper.examtime
    over_time = paper.overtime
    subject_list = studentsubjectlistget(student)
    if now1 > starttime:
        if count == 0:
            if now1 < over_time:
                over_time1 = over_time.strftime('%m/%d/%Y %H:%M:%S')
                fills = paper.fid.all()
                ques = paper.qid.all()
                fill_count = 0
                ques_count = 0
                fill_grade = 0
                ques_grade = 0
                for fill in fills:
                    fill_count += 1
                    fill_grade += fill.score
                for que in ques:
                    ques_count +=1
                    ques_grade += que.score
                return render(request,'exam.html',{'student':student,'paper':paper,'subject':paper.subject,'fill_grade':fill_grade,
                                                   'fill_count':fill_count,'ques_grade':ques_grade,'ques_count':ques_count,'over_time':over_time1})
            else:
                return render(request,'student.html',{'student':student,'flag':'5','subjects':json.dumps(subject_list)})
        else:
            return render(request, 'student.html', {'student': student, 'flag': '7','subjects':json.dumps(subject_list)})

    else :
        return render(request,'student.html',{'student':student,'flag':'6','subjects':json.dumps(subject_list)})


#计算由exam.html模版传过来的数据计算成绩
def calGrade(request):

    if request.method=='POST':
        # 得到学号和科目
        sid=request.POST.get('sid')
        paper_id = request.POST.get('paper_id')
        paper = models.Paper.objects.get(id=paper_id)
        # 防止页面回退和刷新多次获得成绩
        if models.Grade.objects.filter(Q(sid_id=sid) & Q(paper=paper)).count() == 0:
            # 计算该考试的学生成绩
            mygrade = 0  # 初始化一个成绩为0
            #计算该考试的选择题成绩
            questions= paper.qid.all() # 获取试卷的所有选择题
            for p in questions:
                questionanswer = models.QuestionAnswer.objects.filter(Q(pid=paper)&Q(qid=p))[0]
                questionanswer.all +=1
                qId=str(p.id)#int 转 string,通过pid找到题号
                myans=request.POST.get(qId)#通过 qid 得到学生关于该题的作答
                okans=p.answer#得到正确答案
                if myans==okans:#判断学生作答与正确答案是否一致
                    mygrade+=p.score#若一致,得到该题的分数,累加mygrade变量
                    questionanswer.right +=1
                questionanswer.save()
            # 计算该考试的填空题成绩
            fills = paper.fid.all()
            for fill in fills:
                fillquestionanswer = models.FillQuestionAnswer.objects.filter(Q(pid=paper)&Q(fid=fill))[0]
                fillquestionanswer.all +=1
                right = 0
                okans = []
                okans.append(fill.answerA.strip())
                okans.append(fill.answerB.strip())
                okans.append(fill.answerC.strip())
                okans.append(fill.answerD.strip())
                okans.append(fill.answerE.strip())
                okans = okans[0:fill.count]
                for x in range(0,fill.count):
                    fId = str(fill.id)+'_'+str(x+1)
                    myfillans = request.POST.get(fId)
                    if myfillans:
                        myfillans = myfillans.strip()

                    if fill.order == 1:
                        if myfillans == okans[x]:
                            right +=1
                    else:
                        if myfillans in okans:
                            right +=1
                gradetample = (right*fill.score)//fill.count
                if gradetample == fill.score:
                    fillquestionanswer.right +=1
                mygrade += gradetample
                fillquestionanswer.save()

            mygrade = (mygrade*100)//paper.beforegrade
            # 向Grade表中插入数据
            models.Grade.objects.create(sid_id=sid,subject=paper.subject,grade=mygrade,paper=paper)
        # 重新获取该学生信息和学生成绩信息
        student = models.Student.objects.get(id=sid)
        subject_list = studentsubjectlistget(student)
        # 重新渲染index.html模板
        return render(request,'student.html',{'student':student,'flag':0,'subjects':json.dumps(subject_list)})

# 获取能力评级
def getAbilitys(request):
    if request.method == 'GET':
        teaid = request.GET['teacherid']
        subjects = models.Subject.objects.filter(tea_id_id=teaid)
        abilitys_temp = models.Ability.objects.values_list('subject')
        abilitys= assembly(abilitys_temp)
        total = len(subjects)
        row = []
        for x in range(0,total):
            if subjects[x].subject in abilitys:
                row.append({'id':x+1,'subject':subjects[x].subject,'check1':'是'})
            else:
                row.append({'id':x+1,'subject':subjects[x].subject,'check1':'否'})
        data = {"total":total,"rows":row}
        return JsonResponse(data)

# 获取选择题
def questionDataGet(request):
    if request.method=='GET':
        teaid = request.GET['teacherid']
        subjects = models.Subject.objects.filter(tea_id_id=teaid)
        row =[]
        total = 0
        for subject in subjects:
            questions = models.Question.objects.filter(subject=subject.subject)
            total += len(questions)
            for question in questions:
                row.append({'id':question.id,'subject':question.subject, 'ability':question.ability, 'chapter':question.chapter,
                            'title':question.title,'optionA':question.optionA,'optionB':question.optionB,'optionC':question.optionC,'optionD':question.optionD,
                            'answer':question.answer,'level':question.get_level_display(),'score':question.score})
        data = {"total":total,"rows":row}
        return JsonResponse(data)


# 获取填空题
def fillQuestionDataGet(request):
    if request.method=='GET':
        teaid = request.GET['teacherid']
        subjects = models.Subject.objects.filter(tea_id_id=teaid)
        row =[]
        total = 0
        for subject in subjects:
            fillquestions = models.FillQuestion.objects.filter(subject=subject.subject)
            total += len(fillquestions)
            for fillquestion in fillquestions:
                row.append({'id':fillquestion.id,'subject':fillquestion.subject, 'ability':fillquestion.ability,'chapter':fillquestion.chapter,
                            'title':fillquestion.title,'count':fillquestion.count,'answer1':fillquestion.answerA,'answer2':fillquestion.answerB,'answer3':fillquestion.answerC,
                            'answer4':fillquestion.answerD,'answer5':fillquestion.answerE,'level':fillquestion.get_level_display(),'order':fillquestion.get_order_display(),'score':fillquestion.score})
        data = {"total":total,"rows":row}
        return JsonResponse(data)
        pass

 # 增加能力评级
@require_POST
def abilityadd(request):
    if request.method == 'POST':
        chapters=request.POST.get('chapters')
        subject = request.POST.get('subject')
        chapter_list = chapters.split(":")
        for i in range(0,len(chapter_list)-1):
            models.Ability.objects.create(ability=i+1,chapter=chapter_list[i],subject=subject)
        return JsonResponse({'flag':'4'})

# 展示能力评级
@require_POST
def abilityshow(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        abilitys_temp=models.Ability.objects.filter(subject=subject)
        abilitys=[]
        for x in range(0,len(abilitys_temp)):
            abilitys.append({'chapter':abilitys_temp[x].chapter})
        return JsonResponse({'flag':'2','abilitys':abilitys})
# 删除能力评级
@require_POST
def abilitydel(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        models.Ability.objects.filter(subject=subject).delete()
        return JsonResponse({'flag':'3'})

# 增加填空题
@require_POST
def questionadd(request):
    if request.method == 'POST':
        subject= request.POST.get('subject')
        ability_temp= request.POST.get('ability')
        title = request.POST.get('title')
        optionA = request.POST.get('optionA')
        optionB = request.POST.get('optionB')
        optionC = request.POST.get('optionC')
        optionD = request.POST.get('optionD')
        answer = request.POST.get('answer')
        level = request.POST.get('level')
        score = int(request.POST.get('score'))
        abilitylist = models.Ability.objects.filter(Q(subject=subject)&Q(ability=ability_temp))
        ability=abilitylist[0]
        models.Question.objects.create(subject=subject,ability=ability.ability,chapter=ability.chapter,title=title,optionA=optionA,optionB=optionB,optionC=optionC,optionD=optionD,answer=answer,level=level,score=score)
        return JsonResponse({'flag':'1'})

# 增加填空题
@require_POST
def filladd(request):
    if request.method == 'POST':
        subject= request.POST.get('subject')
        ability_temp = request.POST.get('ability')
        title = request.POST.get('title')
        count = int(request.POST.get('count'))
        answers=[]
        answers.append(request.POST.get('answerA'))
        answers.append(request.POST.get('answerB'))
        answers.append(request.POST.get('answerC'))
        answers.append(request.POST.get('answerD'))
        answers.append(request.POST.get('answerE'))
        for a in range(0,5):
            if answers[a]==None:
                answers[a]='#'
        level = request.POST.get('level')
        order = request.POST.get('order')
        score = int(request.POST.get('score'))
        abilitylist = models.Ability.objects.filter(Q(subject=subject)&Q(ability=ability_temp))
        ability=abilitylist[0]
        models.FillQuestion.objects.create(subject=subject,ability=ability.ability,chapter=ability.chapter,count=count,title=title,answerA=answers[0],answerB=answers[1],answerC=answers[2],answerD=answers[3],answerE=answers[4],level=level,order=order,score=score)
        return JsonResponse({'flag':'1'})

# 删除选择题
@require_POST
def questionsdel(request):
    if request.method == 'POST':
        questions = request.POST.get('qusetions')
        questions_list = questions.split(":")
        for x in range(0,len(questions_list)-1):
            question_id = int(questions_list[x])
            models.Question.objects.filter(id=question_id).delete()
        return JsonResponse({'flag':'3'})
# 删除填空题
def fillquestionsdel(request):
    if request.method == 'POST':
        fillquestions = request.POST.get('fillqusetions')
        fillquestions_list = fillquestions.split(":")
        for x in range(0,len(fillquestions_list)-1):
            fillquestion_id = int(fillquestions_list[x])
            models.FillQuestion.objects.filter(id=fillquestion_id).delete()
        return JsonResponse({'flag':'3'})

# 更改选择题
def questionedit(request):
    if request.method == 'POST':
        qusetionid = request.POST.get('id')
        subject = request.POST.get('subject')
        ability_temp = request.POST.get('ability')
        title = request.POST.get('title')
        optionA = request.POST.get('optionA')
        optionB = request.POST.get('optionB')
        optionC = request.POST.get('optionC')
        optionD = request.POST.get('optionD')
        answer = request.POST.get('answer')
        level = request.POST.get('level')
        score = int(request.POST.get('score'))
        abilitylist = models.Ability.objects.filter(Q(subject=subject) & Q(ability=ability_temp))
        ability = abilitylist[0]
        question = models.Question.objects.filter(id=qusetionid)
        question_info ={'subject':subject,'ability':ability.ability, 'chapter':ability.chapter, 'title':title,
                                       'optionA':optionA, 'optionB':optionB, 'optionC':optionC, 'optionD':optionD,
                                       'answer':answer, 'level':level, 'score':score}
        question.update(**question_info)
        return JsonResponse({'flag': '1'})

# 更改填空题
def filledit(request):
    if request.method == 'POST':
        fillid = request.POST.get('id')
        subject = request.POST.get('subject')
        ability_temp = request.POST.get('ability')
        title = request.POST.get('title')
        count = int(request.POST.get('count'))
        answers = []
        answers.append(request.POST.get('answerA'))
        answers.append(request.POST.get('answerB'))
        answers.append(request.POST.get('answerC'))
        answers.append(request.POST.get('answerD'))
        answers.append(request.POST.get('answerE'))
        for a in range(count,5):
           answers[a]='#'
        level = request.POST.get('level')
        order = request.POST.get('order')
        score = int(request.POST.get('score'))
        abilitylist = models.Ability.objects.filter(Q(subject=subject) & Q(ability=ability_temp))
        ability = abilitylist[0]
        fillquestion = models.FillQuestion.objects.filter(id=fillid)
        fillquestion_info ={'subject':subject,'ability':ability.ability,'chapter':ability.chapter,'count':count,'title':title,
        'answerA':answers[0],'answerB':answers[1],'answerC':answers[2],'answerD':answers[3],'answerE':answers[4],'level':level,'order':order,'score':score}
        fillquestion.update(**fillquestion_info)
        return JsonResponse({'flag': '1'})
# 老师获取试卷
def getPapers(request):
    if request.method == 'GET':
        teaid = request.GET['teacherid']
        papers = models.Paper.objects.filter(tid_id=teaid)
        row = []
        total = len(papers)
        for paper in papers:
            row.append({'id':paper.id,'name':paper.name,'subject':paper.subject,'level':paper.get_level_display(),'examtime':paper.examtime,'overtime':paper.overtime})
        data = {"total": total, "rows": row}
        return JsonResponse(data)

# 学生获取试卷
def stugetPapers(request):
    if request.method == 'GET':
        stuid = request.GET['stuid']
        total = 0
        row= []
        now1 = timezone.now()
        subjects = models.Subject.objects.filter(stu_id=stuid)
        for subject in subjects:
            papers = models.Paper.objects.filter(Q(tid=subject.tea_id) & Q(subject=subject.subject))
            total += len(papers)
            for paper in papers:
                row.append(
                    {'id': paper.id, 'name': paper.name, 'subject': paper.subject, 'level': paper.get_level_display(),
                     'examtime': paper.examtime, 'overtime':paper.overtime,'teacher_name':paper.tid.name})
        data = {"total": total, "rows": row}
        return JsonResponse(data)

#获取选择题和填空题的数量
@require_POST
def type_number(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        question_number = len(models.Question.objects.filter(subject=subject))
        fillquestion_number = len(models.FillQuestion.objects.filter(subject=subject))
        return JsonResponse({'flag': '2','question_number':question_number,'fillquestion_number':fillquestion_number})
# 获取对应课程的能力评级的对应参数
def ability_numbers(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        abilitys_temp = models.Ability.objects.filter(subject=subject)
        abilitys = []
        for x in range(0, len(abilitys_temp)):
            numbers = len(models.FillQuestion.objects.filter(Q(subject=subject)&Q(ability=abilitys_temp[x].ability)))+len(models.Question.objects.filter(Q(subject=subject)&Q(ability=abilitys_temp[x].ability)))
            abilitys.append({'numbers':numbers})
        return JsonResponse({'flag':'1','abilitys':abilitys})

# 获取该课程的所有题目
@require_POST
def subject_number_get(request):
    if request.method =='POST':
        subject = request.POST.get('subject')
        number = len(models.Question.objects.filter(subject=subject))+len(models.FillQuestion.objects.filter(subject=subject))
        return JsonResponse({'flag':'1','number':number})

# 组卷以及添加试卷
@require_POST
def paperadd(request):
    if request.method=='POST':
        subject = request.POST.get('paper_subject')
        question_number = int(request.POST.get('question_number'))
        fillquestion_number = int(request.POST.get('fillquestion_number'))
        ability_number_str = request.POST.get('ability_numbers_str')
        name = request.POST.get('paper_name')
        level = request.POST.get('paper_level')
        teacher = request.POST.get('paper_teacher')
        extime = request.POST.get('paper_extime')
        overtime = request.POST.get('paper_overtime')
        print(overtime)
        ability_list_taple = ability_number_str.split(":")
        ability_list = []
        for b in range(0,len(ability_list_taple)-1):
            ability_list.append(int(ability_list_taple[b]))

        # 组卷搜索策略
        level_list = []
        if level == '1':
            level_list = ['1', '2', '3', '4', '5']
        elif level == '2':
            level_list = ['2', '1', '3', '4', '5']
        elif level == '3':
            level_list = ['3', '2', '4', '1', '5']
        elif level == '4':
            level_list = ['4', '3', '5', '2', '1']
        elif level == '5':
            level_list = ['5', '4', '3', '2', '1']


        def complepaper(model1, qnumber): # 组卷算法
            questions = []
            questions_number = 0
            for y in level_list:
                for x in range(0,len(ability_list)):
                    question_tample = model1.objects.filter(Q(subject=subject)&Q(level=y)&Q(ability=x+1))
                    question_tample_number = len(question_tample)
                    if question_tample_number>0:
                        numbercha = qnumber - questions_number
                        ability_number = ability_list[x]
                        if (question_tample_number <= ability_number)&(ability_number>0):
                            if (question_tample_number <= numbercha)&(numbercha>0):
                                for tample in question_tample:
                                    questions.append(tample)
                                questions_number += question_tample_number
                                ability_list[x] -= question_tample_number
                                # print(ability_list,qnumber,'a')
                            elif(question_tample_number > numbercha)&(numbercha>0):
                                resultList = random.sample(range(1, question_tample_number), numbercha)
                                for z in resultList:
                                    questions.append(question_tample[z])
                                ability_list[x] -= numbercha
                                numbercha = 0
                                # print(ability_list,qnumber,'b')
                                break
                            else:
                                continue
                        elif (question_tample_number >ability_number)&(ability_number>0):
                            result_ability_list = random.sample(range(1, question_tample_number), ability_number)
                            if (ability_number <= numbercha)&(numbercha>0):
                                for a in result_ability_list:
                                    questions.append(question_tample[a])
                                questions_number += ability_number
                                ability_list[x] = 0
                                # print(ability_list,qnumber,'c')
                            elif (ability_number > numbercha)&(numbercha>0):
                                resultList1 = random.sample(range(1, ability_number), numbercha)
                                for z in resultList1:
                                    tample1 = result_ability_list[z]
                                    questions.append(question_tample[tample1])
                                ability_list[x] -= numbercha
                                numbercha = 0
                                # print(ability_list,qnumber,'d')
                                break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
                break

            return questions
        quesmodel = models.Question
        choice_list = complepaper(quesmodel, question_number)
        fillmodel = models.FillQuestion
        fill_list = complepaper(fillmodel, fillquestion_number)


        # 计算试卷总分
        beforegrade = 0
        for x in choice_list:
            beforegrade +=x.score
        for y in fill_list:
            beforegrade += y.score
        # 通过 python 时间戳获得独立的试卷独立编号
        pid = int(time.time())
        # 添加试卷
        models.Paper.objects.create(name=name,subject=subject,level=level,examtime=extime,tid_id=teacher,beforegrade=beforegrade,pid=pid,overtime=overtime)
        # 为试卷添加题目
        c= models.Paper.objects.get(pid=pid)
        for x in choice_list:
            c.qid.add(x)
            models.QuestionAnswer.objects.create(pid=c,qid=x)
        for y in fill_list:
            c.fid.add(y)
            models.FillQuestionAnswer.objects.create(pid=c,fid=y)
        return JsonResponse({'flag':1})
# 删除试卷
@require_POST
def paperdel(request):
    if request.method == 'POST':
        papers = request.POST.get('papers')
        papers_list = papers.split(":")
        for x in range(0, len(papers_list) - 1):
            paper_id = int(papers_list[x])
            c = models.Paper.objects.get(id=paper_id)
            c.qid.clear()
            c.fid.clear()
            c.delete()
        return JsonResponse({'flag': '3'})

#查看试卷
def papershow(request):
    paper_id = request.GET.get('paper_id')
    paper = models.Paper.objects.get(id=paper_id)
    now1 = timezone.now()
    over_time = paper.overtime
    if now1 > over_time:
        fills = paper.fid.all()
        ques = paper.qid.all()
        fill_count = 0
        ques_count = 0
        fill_grade = 0
        ques_grade = 0
        for fill in fills:
            fill_count += 1
            fill_grade += fill.score
        for que in ques:
            ques_count += 1
            ques_grade += que.score
        return render(request, 'test.html',
                              { 'paper': paper, 'subject': paper.subject, 'fill_grade': fill_grade,
                               'fill_count': fill_count, 'ques_grade': ques_grade, 'ques_count': ques_count,})
    else:
        return render(request, 'teacher.html', {'teacher': paper.tid,'falg': '6'})


# 老师获取考试信息
@require_POST
def subjectshow(request):
    if request.method =='POST':
        subject = request.POST.get('subject')
        tid = request.POST.get('tid')
        papers = models.Paper.objects.filter(Q(subject=subject)&Q(tid_id=tid))
        papers_list = []
        top=[]
        last = []
        average = []
        for paper in papers:
            papers_list.append(paper.name)
            gradelist = []
            grades = models.Grade.objects.filter(paper=paper)
            for grade in grades:
                gradelist.append(grade.grade)
            top.append(max(gradelist))
            last.append(min(gradelist))
            average.append(sum(gradelist)/len(gradelist))
        return JsonResponse({'paper_name':papers_list,'top':top,'last':last,'average':average})

def studentssubjectshow(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        sid = request.POST.get('sid')
        grades_tample = models.Grade.objects.filter(Q(subject=subject)&Q(sid_id=sid))
        paernamelist = []
        gradelist = []
        for grade in grades_tample:
            paernamelist.append(grade.paper.name)
            gradelist.append(grade.grade)
        return JsonResponse({'paper_name':paernamelist,'grades':gradelist})