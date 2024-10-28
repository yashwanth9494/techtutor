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
            return redirect('myapp:conceptmodel')
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

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def menuconcepts(request):
    concepts = courseconcept.objects.all()
    return render(request,'backend/menuconcept.html', {'concepts':concepts})

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def remove(request,id):
    obj = courseconcept.objects.get(id=id)
    obj.delete()
    return redirect("myapp:menuconcepts")

@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
def updateconcept(request, id):
    obj = courseconcept.objects.get(id = id)
    form = courseconceptform(instance=obj)
    if request.method == 'POST':
        form = courseconceptform(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            return redirect("myapp:menuconcepts")
        else:
            form = coursemodelform(instance = obj)
    return render(request,'backend/concept.html',{'form':form})



