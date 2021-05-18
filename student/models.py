from django.db import models

# Create your models here.
# 为性别,学院,难度 指定备选字段
SEX = (
    ('男', '男'),
    ('女', '女'),
)

LEVEL = {
    ('1', 'easy'),
    ('2', 'normal'),
    ('3', 'difficult'),
    ('4', 'hard'),
    ('5', 'hell'),
}


class Dept(models.Model):
    id = models.AutoField(primary_key=True)
    dept = models.CharField('学院',max_length=20,unique=True)

    class Meta:
        db_table = 'dept'
        verbose_name = '学院'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dept


class Major(models.Model):
    id = models.AutoField(primary_key=True)
    major = models.CharField('专业',max_length=20,unique=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE,blank=True)

    class Meta:
        db_table = 'Major'
        verbose_name = '专业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.major


class Student(models.Model):
    id = models.CharField('学号', max_length=20, primary_key=True)
    name = models.CharField('姓名', max_length=20)
    sex = models.CharField('性别', max_length=4, choices=SEX, default='男')
    dept = models.ForeignKey(Dept,to_field="dept",on_delete=models.CASCADE, blank=True)
    major = models.ForeignKey(Major,to_field="major", on_delete=models.CASCADE, blank=True)
    password = models.CharField('密码', max_length=20, default='111')
    email = models.EmailField('邮箱', blank=True)
    birth = models.DateField('出生日期', default='0001/01/01')

    class Meta:
        db_table = 'student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Teacher(models.Model):
    id = models.CharField("教工号", max_length=20, primary_key=True)
    name = models.CharField('姓名', max_length=20)
    sex = models.CharField('性别', max_length=4, choices=SEX, default='男')
    dept = models.ForeignKey(Dept,to_field="dept",on_delete=models.CASCADE, blank=True)
    email = models.EmailField('邮箱', blank=True)
    password = models.CharField('密码', max_length=20, default='000')
    birth = models.DateField('出生日期',default='0001/01/01')

    class Meta:
        db_table = 'teacher'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    tea_id = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    stu_id = models.ManyToManyField(Student)  # 多对多
    subject = models.CharField('科目', max_length=20)
    major = models.ManyToManyField(Major)

    class Meta:
        db_table = 'Subject'
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class Ability(models.Model):
    id = models.AutoField(primary_key=True)
    ability = models.IntegerField('能力评级')
    chapter = models.CharField('对应章节',max_length=20)
    subject = models.CharField('课程',max_length=20)

    class Meta:
        db_table = 'Ability'
        verbose_name = '能力评级库'
        verbose_name_plural = verbose_name


class Question(models.Model):
    ANSWER = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    id = models.AutoField(primary_key=True)
    subject = models.CharField('科目', max_length=20)
    ability = models.IntegerField('能力评级')
    chapter = models.CharField('对应章节', max_length=20)
    title = models.TextField('题目')
    optionA = models.CharField('A选项', max_length=30)
    optionB = models.CharField('B选项', max_length=30)
    optionC = models.CharField('C选项', max_length=30)
    optionD = models.CharField('D选项', max_length=30)
    answer = models.CharField('答案', max_length=10, choices=ANSWER)
    level = models.CharField('难度等级', max_length=10, choices=LEVEL)
    score = models.IntegerField('分数', default=1)

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题库'
        verbose_name_plural = verbose_name




class FillQuestion(models.Model):
    ORDER=((1,'空格输入有序'),
           (2,'空格输入无序'))
    # 填空题
    id = models.AutoField(primary_key=True)
    subject = models.CharField('科目', max_length=20)
    ability = models.IntegerField('能力评级')
    chapter = models.CharField('对应章节', max_length=20)
    title = models.TextField('题目')
    count = models.IntegerField('空格数',default=1)
    answerA = models.CharField('第一空格答案', max_length=30)
    answerB = models.CharField('第二空格答案', max_length=30)
    answerC = models.CharField('第三空格答案', max_length=30)
    answerD = models.CharField('第四空格答案', max_length=30)
    answerE = models.CharField('第五空格答案', max_length=30)
    level = models.CharField('难度等级', max_length=10, choices=LEVEL)
    score = models.IntegerField('分数', default=1)
    order = models.IntegerField('顺序',choices=ORDER,default=1)

    class Meta:
        db_table = 'fill_question'
        verbose_name = '填空题库'
        verbose_name_plural = verbose_name




class Paper(models.Model):
    # 题号pid 和题库为多对多的关系
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(unique=True,default=-1)
    name = models.CharField('试卷名字',max_length=30)
    qid = models.ManyToManyField(Question)  # 多对多
    fid = models.ManyToManyField(FillQuestion)
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 添加外键
    subject = models.CharField('科目', max_length=20)
    level = models.CharField('难度等级', max_length=10, choices=LEVEL)
    examtime = models.DateTimeField()
    beforegrade = models.IntegerField(default=0)
    overtime = models.DateTimeField(default=None)

    class Meta:
        db_table = 'paper'
        verbose_name = '试卷'
        verbose_name_plural = verbose_name




class Grade(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, default='')  # 添加外键
    subject = models.CharField('科目', max_length=20)
    grade = models.IntegerField()
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return '<%s:%s>' % (self.sid, self.grade)

    class Meta:
        db_table = 'grade'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name


class QuestionAnswer(models.Model):
    pid =  models.ForeignKey(Paper, on_delete=models.CASCADE)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    all = models.IntegerField(default=0)
    right = models.IntegerField(default=0)

    class Meta:
        db_table = 'qusetion_answer'
        verbose_name = '选择题答题情况'
        verbose_name_plural = verbose_name


class FillQuestionAnswer(models.Model):
    pid = models.ForeignKey(Paper, on_delete=models.CASCADE)
    fid = models.ForeignKey(FillQuestion, on_delete=models.CASCADE)
    all = models.IntegerField(default=0)
    right = models.IntegerField(default=0)

    class Meta:
        db_table = 'fill_qusetion_answer'
        verbose_name = '填空题答题情况'
        verbose_name_plural = verbose_name