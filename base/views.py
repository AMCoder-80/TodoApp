from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.


def first(request):
    return HttpResponse("My Todo List app")


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_result = self.request.GET.get('search_bar', '')
        if search_result:
            context['tasks'] = Task.objects.filter(title__icontains=search_result)
        context['search_bar'] = search_result
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'start_time', 'end_time', 'priority', 'complete']
    success_url = reverse_lazy('base:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'start_time', 'end_time', 'priority', 'complete']
    template_name = 'base/task_update.html'
    success_url = reverse_lazy('base:task_list')
    context_object_name = 'task'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('base:task_list')


class LoginUser(LoginView):
    template_name = 'base/Login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:task_list')


class UserCreation(FormView):
    template_name = 'base/Register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('base:task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user=user)
        return super(UserCreation, self).form_valid(form)

    def get(self, *arg, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:task_list')
        return super(UserCreation, self).get(*arg, **kwargs)
