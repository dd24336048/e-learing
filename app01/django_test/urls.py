"""
URL configuration for django_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from app01 import views
from django.urls import path, include
urlpatterns = [
   path('', views.index, name='index'),
   path('admin/',admin.site.urls),
   path('register/',views.sign_up,name='Register'),
   path('login',views.sign_in,name='Login'),
   path('logout',views.log_out,name='Logout'),
   path('search/',views.word_search,name='Search'),
   path('starExam',views.starExam,name='開始考試'),
   path('submit_exam',views.submit_exam,name='submit_exam'),
   path('generate_exam_papers_by_year',views.generate_exam_papers_by_year,name = '考試開始'),
   path('select_testpaper/',views.select_testpaper,name='選擇考卷'),
   path('exam_paper/',views.exam_paper,name='查看考卷'),
   path('test_paper',views.test_paper,name='考卷內容'),
   path('112_testpaper',views.testpaper112,name='112年學測'),
   path('111_testpaper',views.testpaper111,name='111年學測'),
   path('110_testpaper',views.testpaper110,name='110年學測'),
   path('109_testpaper',views.testpaper109,name='109年學測'),
   path('108_testpaper',views.testpaper108,name='108年學測'),
   path('107_testpaper',views.testpaper107,name='107年學測'),
   path('106_testpaper',views.testpaper106,name='106年學測'),
   path('105_testpaper',views.testpaper105,name='105年學測'),
   path('104_testpaper',views.testpaper104,name='104年學測'),
   path('103_testpaper',views.testpaper103,name='103年學測'),
]
