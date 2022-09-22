from gc import get_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# UserCreationForm sirve para crear un formulario de registro de usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate , logout
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.   


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registro de usuario
                # create_user sirve para crear un usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) #Esto es para crear una sesion en las cookies y poder usar esa usuario
                return redirect('tasks')
            except:
                form = UserCreationForm()
                return render(request, 'signup.html', {'form': form, 'error': 'El usuario ya existe'})
            # mensaje de error
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form, 'error': 'Las contraseñas no coinciden'})

#@login_required(login_url='signup') esta forma es para indicarle la ruta a la cual va redirigir si no esta logueado
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) #Esto es para filtrar las tareas por usuario y por fecha de completado
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') #Esto es para filtrar las tareas por usuario y por fecha de completado
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def signout(request):
    logout(request) #Esto es para cerrar la sesion
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm(), 'error': 'El usuario o la contraseña no son correctos'})
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create(request):
    if request.method == 'GET':
        form = CreateTaskForm()
        return render(request, 'create_task.html', {'form': form})
    else:
        try:
            form = CreateTaskForm(request.POST) #Esto es para crear un formulario a partir de un modelo
            newtask = form.save(commit=False)   #commit=False sirve para que no guarde los datos en la base de datos, solo los guarde en la variable newtask
            newtask.user = request.user #Esto es para guardar el usuario que creo la tarea
            newtask.save()  #Esto es para guardar los datos en la base de datos
            return redirect('tasks') 
        except ValueError: 
            return render(request, 'create_task.html', {'form': CreateTaskForm(), 'error': 'Datos incorrectos'})


@login_required
def task_detail(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=id, user=request.user) #Esto es para obtener un objeto de la base de datos, si no existe el objeto, devuelve un error 404
        form = CreateTaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=id, user=request.user)
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Datos incorrectos'})

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now() #Esto es para guardar la fecha de completado y timezone.now() es para guardar la fecha actual
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')