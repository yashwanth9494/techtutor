from django.shortcuts import render,redirect,HttpResponse
from myapp.models import coursemodel
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def gethome(request):
    user = request.user
    courses = coursemodel.objects.all()

    if user.is_authenticated:
        # User is logged in
        cartitems = list(add_to_cart.objects.filter(userid=user).values_list("courseid", flat=True))
        enrolleditems = list(enrolled_courses.objects.filter(userid=user).values_list("courseid", flat=True))
    else:
        # User is anonymous
        cartitems = []
        enrolleditems = []

    return render(request, 'frontend/home.html', {
        'courses': courses,
        'cartitems': cartitems,
        "enrolleditems": enrolleditems
    })


def getcourses(request):
    user = request.user
    courses = coursemodel.objects.all()

    if user.is_authenticated:
        # User is authenticated, fetch cart and enrolled courses
        cartitems = list(add_to_cart.objects.filter(userid=user).values_list("courseid", flat=True))
        enrolleditems = list(enrolled_courses.objects.filter(userid=user).values_list("courseid", flat=True))
    else:
        # User is not authenticated, return empty cart and enrolled items
        cartitems = []
        enrolleditems = []

    return render(request, 'frontend/coursecard.html', {
        'courses': courses,
        'cartitems': cartitems,
        'enrolleditems': enrolleditems
    })


def registrationview(request):
    f = regform()
    if request.method == 'POST':
        f1 = regform(request.POST)
        
        if f1.is_valid():
            f1.save()
            return redirect('login')
    return render(request, 'frontend/register.html', {'f':f})



def loginview(request):
    f = loginform()
    if request.method == 'POST':
        f1 = loginform(request.POST)
        if f1.is_valid():
            email = f1.cleaned_data['email']
            password = f1.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('gethome')
            else:
                data='invalid user'
                return render(request, 'frontend/login.html', {'f': f,'data':data,'x':email})
    return render(request, 'frontend/login.html', {'f': f})


@login_required(login_url='/login/')
def profile(request):
    return render(request,'frontend/profile.html',{'user': request.user})

@login_required(login_url='/login/')
def logoutview(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def updateview(request,id):
    obj = CustomUser.objects.get(id=id)
    f = Updateform(instance=obj)
    if request.method=="POST":
        f1 = Updateform(request.POST,instance=obj)
        if f1.is_valid():
            f1.save()
            return redirect('profile')
        else:
            f = Updateform(instance=obj)
    return render(request, 'frontend/update.html',{'f':f})

@login_required(login_url='/login/')
def deleteview(request, id):
    obj = CustomUser.objects.get(id=id)
    obj.delete()
    return redirect('gethome')   


def changepassword(request, value=None):
    if value:
        try:
            # Case 1: User identifier (email) is provided, fetch user
            obj = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            return HttpResponse('User not found', status=404)
    else:
        obj = None  # Case 2: No identifier provided, expect user to enter details

    if request.method == "POST":
        # If an identifier is provided, bind form to that user instance
        if obj:
            f = changepasswordform(request.POST, instance=obj)
        else:
            # If no identifier, create form without instance and validate user input
            f = changepasswordform(request.POST)

        if f.is_valid():
            # If form is valid, save the password change
            if obj:
                # Case 1: Directly save the new password
                f.save()
            else:
                # Case 2: Fetch user by email entered in form
                email = f.cleaned_data.get('email')
                try:
                    obj = CustomUser.objects.get(email=email)
                    # Update the instance with the new password
                    obj.set_password(f.cleaned_data.get('password'))
                    obj.save()
                except CustomUser.DoesNotExist:
                    return HttpResponse('User not found', status=404)
            return redirect('login')
    else:
        # Initialize the form for GET requests
        f = changepasswordform(instance=obj) if obj else changepasswordform()

    return render(request, 'frontend/changepassword.html', {'f': f})


@login_required(login_url='/login/')
def addtocartview(request,id):
    user = request.user
    course = coursemodel.objects.get(id=id)
    addtocart = add_to_cart.objects.create(userid=user, courseid=course)
    return redirect('getcourses')


@login_required(login_url='/login/')
def cartview(request):
    user = request.user
    usercart = add_to_cart.objects.filter(userid=user)
    total_price = sum(item.courseid.courseprice for item in usercart)
    return render(request, 'frontend/cart.html',{'usercart':usercart, 'total_price':total_price})

@login_required(login_url='/login/')
def removecartitem(request, id):
    user = request.user
    cartitem = add_to_cart.objects.get(userid=user,id=id)
    cartitem.delete()
    return redirect('cartview')

@login_required(login_url='/login/')
def checkoutview(request, id=None):
    user = request.user
    if id==None:
        cartitems = add_to_cart.objects.filter(userid=user)
        total_price = sum(item.courseid.courseprice for item in cartitems)
    else:
        cartitems = coursemodel.objects.filter(id=id)
        total_price = cartitems[0].courseprice

    context={
        "cartitems":cartitems,
        "total_price":total_price,
        "id":id
    }
    return render(request, 'frontend/checkout.html', context)


@login_required(login_url='/login/')
def enroll(request,id=None):
    user = request.user
    items=None
    if request.method == 'POST':
        if id==None:
            items = add_to_cart.objects.filter(userid=user).select_related('courseid')
            for item in items:
                    if not enrolled_courses.objects.filter(userid=user, courseid=item.courseid).exists():
                        enrolled_courses.objects.create(userid=user, courseid=item.courseid)
            items.delete()
            return redirect("enrolledcourses")
        else:
            items=coursemodel.objects.get(id=id)
            cartitem=add_to_cart.objects.filter(userid=user,courseid=items)
            if not enrolled_courses.objects.filter(userid=user, courseid=items).exists():
                enrolled_courses.objects.create(userid=user, courseid=items)
            cartitem.delete()
            return redirect("enrolledcourses")
    

@login_required(login_url='/login/')
def enrolledcourses(request):
    user = request.user
    items = enrolled_courses.objects.filter(userid=user)
    enrolleditems = list(enrolled_courses.objects.filter(userid=user).values_list("courseid",flat=True))
    cartitems = list(add_to_cart.objects.filter(userid=user).values_list("courseid", flat=True))
    context={
        "items":items,
        "enrolleditems":enrolleditems,
        "cartitems":cartitems,
    }
    return render(request,'frontend/enrolledcourses.html',context)

