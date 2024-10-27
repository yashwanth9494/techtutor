from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def create_concept(request):
    ff = courseconceptform()
    if request.method == 'POST':
        ff1 = courseconceptform(request.POST)
        if ff1.is_valid():
            ff1.save()
            return HttpResponse("concept added")
    return render(request,'backend/concept.html',{'ff':ff})

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def create_course(request):
    f = coursemodelform()
    if request.method == "POST":
        f1 = coursemodelform(request.POST, request.FILES)
        if f1.is_valid():
            f1.save()
            return redirect("myapp:menu")
    return render(request,'backend/course.html',{'f':f})

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def menu(request):
    courses = coursemodel.objects.all()
    return render(request,'backend/menu.html', {'courses':courses})

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def delete(request, id):
    obj = coursemodel.objects.get(id=id)
    obj.delete()
    return redirect('myapp:menu')

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def update(request, id):
    obj = coursemodel.objects.get(id = id)
    form = coursemodelform(instance=obj)
    if request.method == 'POST':
        form = coursemodelform(request.POST,request.FILES, instance = obj)
        if form.is_valid():
            form.save()
            return redirect("myapp:menu")
        else:
            form = coursemodelform(instance = obj)
    return render(request,'backend/update.html',{'form':form})