from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import medicalForm
from .models import medical
import re
from datetime import datetime
from django.utils import timezone
# Create your views here.

def SignupPage(request):
    error_message = None
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')  
        password_pattern = re.compile(r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>a-zA-Z])') 
        if not uname or not email or not pass1 or not pass2:
            error_message = "All fields are required!"
        elif pass1 != pass2:
            error_message = "Your password and confirm password are not the same!"
        elif not password_pattern.match(pass1):
            error_message = "Password should contain at least one number, one special character, and alphabets!"
        else:
            if User.objects.filter(username=uname).exists():
                error_message = "Username already exists!"
            elif User.objects.filter(email=email).exists():
                error_message = "Email already exists!"
            else:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
    return render(request, 'signup.html', {'error_message': error_message})


def LoginPage(request):
    error_message = None
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if not username  or not pass1:
            error_message = "All fields are required!"
        elif user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = "Your password or username is incorrect!"
    return render (request,'login.html',{'error_message': error_message})


@login_required(login_url='/login/')
def HomePage(request):
    username = request.user.username
    current_datetime =datetime.now()
    return render (request,'home.html',{'username' : username , 'current_datetime':current_datetime})


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def list(request):
    data=medical.objects.all()
    today = timezone.now().date()
    return render(request,'app2/list.html',{'data' : data , 'today':today})


@login_required(login_url='login')
def Add(request):
    if request.method == 'POST':
        form = medicalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form =medicalForm()
    return render(request, 'app2/add.html', {'form': form})


@login_required(login_url='login')
def Delete_record(request,pk):
    medicine=medical.objects.get(pk=pk)  
    if request.method == 'POST':
        medicine.delete()
        return redirect('list')
    return render(request,'app2/list.html',{'medical':medical})


@login_required(login_url='login')
def Update_Record(request,id):
    if request.method=='POST':
        data=medical.objects.get(pk=id)
        form=medicalForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        data=medical.objects.get(pk=id)
        form=medicalForm(instance=data)
    return render(request,'app2/update.html',{'form':form,})


@login_required(login_url='login')
def Search(request):
    query = request.GET.get('q')
    if query:
        medicines = medical.objects.filter(name__istartswith=query)
    else:
        medicines = medical.objects.all()
    return render(request, 'app2/search.html', {'medicines': medicines, 'query': query})


