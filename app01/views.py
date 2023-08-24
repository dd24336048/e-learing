from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("歡迎使用112")

def login(request):
    return render(request,"login.html")