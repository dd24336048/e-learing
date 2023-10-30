from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from.forms import RegisterForm
from.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
#from .models import EnglishWord
from django.http import JsonResponse
from django.db.models import Q
#from . models import Testpaper
#from . models import Academic
from . models import  student_scores
from django.contrib.auth.models import User
from datetime import datetime
from .models import EnglishOptionalNumber1,EnglishOptionalNumber2,EnglishOptional,EnglishOptionalNumber3,EnglishOptionalNumber4,EnglishOptionalNumber5,OptionalTopicNumber2,OptionalTopicNumber3,OptionalTopicNumber5,ExamPaper,ExamPapers
from django.shortcuts import render
from django.db.models import Q



@login_required(login_url="Login")
# Create your views here.
def index(request):
    return render(request,"home.html")
#註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request,'register.html', context)
#登入
def sign_in(request):

    form = LoginForm()

    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')

    context ={
        'form':form
    }

    return render(request,'login.html',context)

#登出
def log_out(request):

    logout(request)
    return redirect('Login')
 #搜尋單字系統
def word_search(request):
    # if request.method == 'GET':
    #     query = request.GET.get('query', '')  # 获取用户输入的查询词

    #     # 使用Q对象进行模糊搜索
    #     english_words = EnglishWord.objects.filter(Q(word__icontains=query) | Q(meaning__icontains=query))

    #     context = {
    #         'query': query,
    #         'english_words': english_words,
    #     }

    #     return render(request, 'search.html', context)
    
    return render(request, 'search.html')  # 渲染搜索页面
#考試介面
def starExam(request):
    exam_papers = Academic.objects.all()
    
    
    return render(request, 'exam.html', {'exam_papers': exam_papers})

import re  # 导入正则表达式模块

# ...

from datetime import datetime
from .models import student_scores, EnglishOptionalNumber1

def submit_exam(request):
    if request.method == 'POST':
        stu_answers = request.POST
        year = request.POST.get("year")
        now = datetime.now()
        correct_answers = {}
        stu_grade = 0

        # 获取该年份的考卷正确答案
        exam_paper = EnglishOptionalNumber1.objects.filter(year=year)
        for question in exam_paper:
            correct_answers[question.id] = question.answer
        
        # 逐个比较学生答案和正确答案
        for question_id, stu_answer_list in stu_answers.items():
            if question_id.startswith("paper_"):  # 检查是否是问题答案字段
               question_number = int(question_id.replace("paper_", ""))  # 获取问题编号
               correct_answer = correct_answers.get(question_number)

               if correct_answer and stu_answer_list:
                  stu_answer = stu_answer_list[0]  # 从列表中获取答案
                  if stu_answer == correct_answer:  # 比较答案
                     stu_grade += 1



                
        # 保存学生成绩记录
        record_grade = student_scores(subject=year, score=stu_grade, timestamp=now)
        record_grade.save()
        
        print(str(stu_answers) + "答案")
        print(question_number)
        print(correct_answers)
        print(stu_grade)
       
    return render(request, 'submit.html', {'stu_grade': stu_grade})

def generate_exam_papers_by_year(request):
    paper_models = [
        (EnglishOptionalNumber1, 'questions_optional_number1'),
        (EnglishOptionalNumber2, 'questions_optional_number2'),
        (EnglishOptionalNumber3, 'questions_optional_number3'),
        (EnglishOptionalNumber4, 'questions_optional_number4'),
        (EnglishOptionalNumber5, 'questions_optional_number5')
    ]
    
    exam_papers_by_year = []

    for model, field_name in paper_models:
        years = model.objects.values_list('year', flat=True).distinct()
        
        for year in years:
            questions = model.objects.filter(year=year)
            
            exam_paper = ExamPaper.objects.create(name=f"Exam {year}", description=f"Exam paper for the year {year}")
            field = getattr(exam_paper, field_name)
            field.add(*questions)
            
            exam_papers_by_year.append(exam_paper)

    return render(request, 'exam_papers_by_year.html', {'exam_papers_by_year': exam_papers_by_year})

def select_testpaper(request):
    years = set(EnglishOptionalNumber1.objects.values_list('year', flat=True))
    if request.method =='POST':
        select_year = request.GET.get('year')
        exam_papers = ExamPaper.objects.filter(name=f"Exam {select_year}") 
        return render(request,'exam_paper.html',{exam_papers : exam_papers})
    return render(request, 'select_testpaper.html', {'years': years})


def exam_paper(request):
    year = request.POST.get('year')
    exam_papers = ExamPaper.objects.filter(name=f"Exam{year}")
    return render(request,'exam_paper.html',{'exam_paper':exam_papers})
                   
def test_paper(request):
    if request.method == 'POST':
        selected_year = request.POST.get('year')
        test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
        exam_testpaper_year = []
        for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPaper.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)

        return render(request, 'test_paper.html', {'exam_testpaper_year': exam_testpaper_year})
    
    # 当 GET 请求时，渲染包含选择年份表单的页面
    exam_papers = ExamPaper.objects.all()
    return render(request, 'test_paper.html', {'exam_papers': exam_papers})

def testpaper112(request):
    selected_year = '112'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="112-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="112-2")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="112-1")
    group5_1 = OptionalTopicNumber5.objects.get(topic_number="112-1")
    group5_2 = OptionalTopicNumber5.objects.get(topic_number="112-2")
    group5_3 = OptionalTopicNumber5.objects.get(topic_number="112-3")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group3_1': group3_1,
            'group5_1': group5_1,
            'group5_2': group5_2,
            'group5_3': group5_3,
            'selected_year':selected_year
        }
    return render(request, 'testpaper112.html',context)
def testpaper111(request):
    selected_year = '111'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="111-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="111-2")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="111-1")
    group5_1 = OptionalTopicNumber5.objects.get(topic_number="111-1")
    group5_2 = OptionalTopicNumber5.objects.get(topic_number="111-2")
    group5_3 = OptionalTopicNumber5.objects.get(topic_number="111-3")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group3_1': group3_1,
            'group5_1': group5_1,
            'group5_2': group5_2,
            'group5_3': group5_3,
        }
    return render(request, 'testpaper111.html',context)
def testpaper110(request):
    selected_year = '110'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="110-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="110-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="110-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="110-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper110.html',context)

def testpaper109(request):
    selected_year = '109'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="109-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="109-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="109-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="109-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper109.html',context)

def testpaper108(request):
    selected_year = '108'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="108-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="108-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="108-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="108-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)
def testpaper107(request):
    selected_year = '107'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="107-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="107-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="107-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="107-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)

def testpaper106(request):
    selected_year = '106'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="106-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="106-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="106-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="106-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)

def testpaper105(request):
    selected_year = '105'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="105-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="105-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="105-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="105-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)

def testpaper104(request):
    selected_year = '104'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="104-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="104-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="104-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="104-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)
def testpaper103(request):
    selected_year = '103'
    test_papers_models = [
            (EnglishOptionalNumber1, 'questions_optional_number1'),
            (EnglishOptionalNumber2, 'questions_optional_number2'),
            (EnglishOptionalNumber3, 'questions_optional_number3'),
            (EnglishOptionalNumber4, 'questions_optional_number4'),
            (EnglishOptionalNumber5, 'questions_optional_number5'),
            (OptionalTopicNumber2  , 'questions_optionaltopic_number2'),
            (OptionalTopicNumber3  , 'questions_optionaltopic_number3'),
            (OptionalTopicNumber5  , 'questions_optionaltopic_number5'),
        ]
    exam_testpaper_year = []
    for models, field_name in test_papers_models:
            years = models.objects.filter(year=selected_year).values_list('year', flat=True).distinct()
            for year in years:
                questions = models.objects.filter(year=year)

                exam_paper = ExamPapers.objects.create(
                    name=f"Exam {year} ({selected_year})", 
                    description=f"Exam paper for the year {year}"
                )
                field = getattr(exam_paper, field_name)
                field.add(*questions)
                exam_testpaper_year.append(exam_paper)
    group2_1 = OptionalTopicNumber2.objects.get(topic_number="103-1")
    group2_2 = OptionalTopicNumber2.objects.get(topic_number="103-2")
    group2_3 = OptionalTopicNumber2.objects.get(topic_number="103-3")
    group3_1 = OptionalTopicNumber3.objects.get(topic_number="103-1")
    context = {
            'exam_testpaper_year': exam_testpaper_year,
            'group2_1': group2_1,
            'group2_2': group2_2,
            'group2_3': group2_3,
            'group3_1': group3_1,
            
        }
    return render(request, 'testpaper108.html',context)