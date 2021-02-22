from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


class IndexView(generic.ListView):
    # mainpage view(list of groups)
    template_name = 'tasks/index.html'
    form_class = AddGroupForm
    model = Group

    def get_queryset(self):
        return self.groups.order_by('title')
    
    def get(self, request):
        self.groups = Group.objects.all().order_by('title')
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form, 'groups': self.groups})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form, 'groups': self.groups})


class GroupView(generic.ListView):
    # page of a group(list of tasks)
    template_name = 'tasks/group.html'
    form_class = AddTaskForm
    model = Task

    def get_queryset(self):
        return self.tasks.order_by('-completed', 'title')
    
    def get(self, request, pk):
        self.group_id = pk
        self.tasks = Group.objects.get(pk=pk).task_set.all()
        form = self.form_class(request.GET, pk)
        return render(request, self.template_name, {'form': form, 'tasks': self.tasks})
    
    def post(self, request, pk):
        form = self.form_class(request.POST, pk)
        if form.is_valid():
            form = form.save(commit=False)
        form.group_id = pk
        form.save()
        return redirect(reverse('tasks:group', args=[pk]))


class DeleteGroupView(generic.DetailView):
    template_name = 'tasks/delete_group.html'
    model = Group

    def get_queryset(self):
        return self.groups.order_by('title')
    
    def get(self, request, pk):
        Group.objects.get(id=pk).delete()
        return redirect(reverse('tasks:index'))


class UpdateGroupView(generic.DetailView):
    template_name = 'tasks/update_group.html'
    model = Group
    form_class = AddGroupForm 

    def get_queryset(self):
        return self.groups.order_by('title')
    
    def get(self, request, pk):
        this_group = Group.objects.get(id=pk)

        form = self.form_class(instance=this_group)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, pk):
        this_group = Group.objects.get(id=pk)

        form = self.form_class(request.POST, instance=this_group)
        if form.is_valid():
            form.save()
            return redirect(reverse('tasks:index'))
        return redirect('/')


class UpdateTaskView(generic.DetailView):
    template_name = 'tasks/update_task.html'
    model = Task
    form_class = AddTaskForm

    def get_queryset(self):
        return self.tasks.order_by('title')
    
    def get(self, request, pk):
        this_task = Task.objects.get(id = pk)

        form = self.form_class(instance=this_task)

        return render(request, self.template_name, {'form': form})
    
    def post(self, request, pk):
        this_task = Task.objects.get(id=pk)
        group_pk = this_task.group_id
        form = self.form_class(request.POST, instance=this_task)
        if form.is_valid():
            form.save()
            return redirect(reverse('tasks:group', args=[group_pk]))
        return redirect('/')


class DeleteTaskView(generic.DetailView):
    template_name = 'tasks/delete_task.html'
    model = Task
    
    def get_queryset(self):
        return self.tasks.order_by('title')
    
    def get(self, request, pk):
        this_task = Task.objects.get(id=pk)
        Task.objects.get(id=pk).delete()
        group_pk = this_task.group_id
        return redirect(reverse('tasks:group', args=[group_pk])) 

