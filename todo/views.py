from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ToDo
from .forms import ToDoForm

def todo_list(request):
    todos = ToDo.objects.all().order_by('-id')
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = ToDoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_update(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = ToDoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_delete(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo/todo_delete.html', {'todo': todo})

@csrf_exempt
def todo_toggle_completed(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        completed = request.POST.get('completed') == 'true'
        todo.completed = completed
        todo.save()
        return JsonResponse({'completed': todo.completed})
    return JsonResponse({'error': 'Xatolik'}, status=400)