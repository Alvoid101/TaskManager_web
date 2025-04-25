from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Link, Category, Task
from .forms import TaskForm

# Asegura que la vista index requiere autenticación

@login_required
def index(request):
    # Cargar categorías y enlaces para el usuario actual
    categories = Category.objects.filter(user=request.user)
    links = Link.objects.filter(user_id=request.user)
    tasks = Task.objects.filter(user_id=request.user, finished=False).order_by('-delivery_date')
    finished_tasks = Task.objects.filter(user_id=request.user, finished=True)
    
    return render(request, 'task/index.html', {
        'tasks' : tasks,
        'finished_tasks' : finished_tasks,
        'categories': categories,
        'links': links
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'task/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Validar que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'task/register.html')
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return render(request, 'task/register.html')
            
        # Verificar si el email ya existe
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'task/register.html')
        
        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Iniciar sesión automáticamente
        login(request, user)
        messages.success(request, 'Cuenta creada satisfactoriamente')
        return redirect('index')
        
    return render(request, 'task/register.html')

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        if name:
            Category.objects.create(user=request.user, name=name)
            messages.success(request, 'Categoría creada correctamente')
            return redirect('index')
        messages.error(request, 'Debes indicar un nombre')
    # GET: mostrar formulario
    return render(request, 'task/add_category.html')

@login_required
def edit_category(request, category_id):
    # Obtener la categoría o devolver 404 si no existe o no pertenece al usuario
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        new_name = request.POST.get('category_name')
        if new_name:
            # Verificar si ya existe otra categoría con ese nombre para el mismo usuario
            if Category.objects.filter(user=request.user, name=new_name).exclude(id=category_id).exists():
                messages.error(request, f'Ya tienes una categoría llamada "{new_name}".')
            else:
                category.name = new_name
                category.save()
                messages.success(request, 'Categoría actualizada correctamente.')
                return redirect('index')
        else:
            messages.error(request, 'El nombre no puede estar vacío.')
        # Si hay error en POST, se vuelve a renderizar el form con el error
        return render(request, 'task/edit_category.html', {'category': category})

    # Si es GET, mostrar el formulario prellenado
    return render(request, 'task/edit_category.html', {'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        # Eliminar la categoría
        category_name = category.name # Guardar nombre para mensaje
        category.delete()
        messages.success(request, f'Categoría "{category_name}" eliminada correctamente.')
        return redirect('index')

    # Si es GET, mostrar la página de confirmación
    return render(request, 'task/delete_category.html', {'category': category})
@login_required
def add_link(request, category_id):
    # Obtener la categoría a la que pertenece el enlace
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        link_name = request.POST.get('link_name')
        link_content = request.POST.get('link_content') # Asumiendo que este es el campo para la URL

        if link_name and link_content:
            # Crear el nuevo enlace asociado al usuario y la categoría
            Link.objects.create(
                user_id=request.user,
                category=category,
                name=link_name,
                content=link_content
            )
            messages.success(request, f'Enlace "{link_name}" añadido a la categoría "{category.name}".')
            return redirect('index') # Redirigir de vuelta al index
        else:
            messages.error(request, 'Debes proporcionar un nombre y una URL para el enlace.')
            # Si hay error, volver a mostrar el formulario con el mensaje
            return render(request, 'task/add_link.html', {'category': category})

    # Si es GET, mostrar el formulario vacío, pasando la categoría para saber dónde se añade
    return render(request, 'task/add_link.html', {'category': category})


@login_required
def edit_link(request, link_id):
    # Obtener el enlace o 404 si no existe o no pertenece al usuario
    link = get_object_or_404(Link, id=link_id, user_id=request.user)
    # Obtener todas las categorías del usuario para el selector (opcional)
    user_categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        link_name = request.POST.get('link_name')
        link_content = request.POST.get('link_content')
        category_id = request.POST.get('link_category') # Nuevo campo para cambiar categoría

        if link_name and link_content:
            link.name = link_name
            link.content = link_content
            # Actualizar categoría si se seleccionó una válida
            if category_id:
                try:
                    new_category = Category.objects.get(id=category_id, user=request.user)
                    link.category = new_category
                except Category.DoesNotExist:
                    messages.error(request, 'La categoría seleccionada no es válida.')
                    # Volver a renderizar con error sin guardar otros cambios
                    return render(request, 'task/edit_link.html', {
                        'link': link,
                        'user_categories': user_categories
                    })
            else: # Si no se selecciona categoría, dejarla como está o ponerla null
                 link.category = None # Opcional: decidir qué hacer si no se elige categoría

            link.save()
            messages.success(request, f'Enlace "{link.name}" actualizado correctamente.')
            return redirect('index')
        else:
            messages.error(request, 'El nombre y la URL del enlace son requeridos.')
            # Volver a renderizar con error
            return render(request, 'task/edit_link.html', {
                'link': link,
                'user_categories': user_categories
            })

    # Si es GET, mostrar el formulario prellenado
    return render(request, 'task/edit_link.html', {
        'link': link,
        'user_categories': user_categories
    })


@login_required
def delete_link(request, link_id):
    link = get_object_or_404(Link, id=link_id, user_id=request.user)

    if request.method == 'POST':
        link_name = link.name # Guardar nombre para mensaje
        link.delete()
        messages.success(request, f'Enlace "{link_name}" eliminado correctamente.')
        return redirect('index')

    # Si es GET, mostrar la página de confirmación
    return render(request, 'task/delete_link.html', {'link': link})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # No guarda aún en la BD
            task.user = request.user  # Asigna el usuario autenticado
            task.save()  # Guarda en la BD
            return redirect('index')
    else:
        form = TaskForm()
        
    return render(request, 'task/create_task.html', {'form':form})

@login_required
def read_task(request, task_id):
    task = Task.objects.get(id=task_id)
    
    return render(request, 'task/view_task.html', {'task':task})

@login_required
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('read_task', task_id=task.id)
    else:
        form = TaskForm(instance=task)
        
    return render(request, 'task/update_task.html', {'form':form, 'task':task})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id = task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'task/delete_task.html', {'task':task})

@login_required
def delete_finished_tasks(request):
    tasks = Task.objects.filter(user_id=request.user, finished=True)
    if request.method == 'POST':
        tasks.delete()
        return redirect('index')
    
    return render(request, 'task/delete_finished_tasks.html')

@login_required
def finish_unfinish_task(request, task_id):
    task = Task.objects.get(id = task_id)

    if request.method == 'POST':
        if task.finished == True:
            task.finished = False
        else:
            task.finished = True
        
        task.save()
        return redirect('index')
    
    return render(request, 'task/finish_unfinish_task.html', {'task':task})