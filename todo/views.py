from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, TaskForm
from .models import Task
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import Alarm

def home(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    return render(request, 'dashboard.html', {'form': form})

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_login')
    return render(request, 'register.html', {'form': form})
def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'my-login.html', {'form': form})

@login_required(login_url='my_login')
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required(login_url='my_login')
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='my_login')
def update_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='my_login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'task_confirm_delete.html', {'task': task})

def user_logout(request):
    logout(request)
    return redirect('home')

def send_email_view(request):
    if request.method == 'POST':
        subject = 'Task Monitor App: Task Happening Soon'
        message = 'You have a task coming up!'
        from_email = 'foursoftfoursoft@example.com'
        recipient_list = ['foursoftfoursoft@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent successfully')

def alarm_list(request):
    alarms = Alarm.objects.all()
    return render(request, 'alarm_list.html', {'alarms': alarms})

def add_alarm(request):
    if request.method == 'POST':
        time = request.POST['time']
        alarm = Alarm.objects.create(time=time)
        return redirect('alarm_list')
    return render(request, 'add_alarm.html')

def delete_alarm(request, pk):
    alarm = Alarm.objects.get(pk=pk)
    alarm.delete()
    return redirect('alarm_list')
