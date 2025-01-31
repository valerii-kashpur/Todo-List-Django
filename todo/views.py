from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from todo.forms import TaskForm, TagForm
from todo.models import Task, Tag


class TaskListView(ListView):
    model = Task
    queryset = (
        Task.objects.all()
        .prefetch_related('tags')
        .order_by('is_done', '-created_at')
    )


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task-list")


def toggle_task_status(request, pk):
    task = Task.objects.get(id=pk)
    task.is_done = not task.is_done
    task.save()

    return HttpResponseRedirect(reverse_lazy("todo:task-list"))


class TagListView(ListView):
    model = Tag


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm

    success_url = reverse_lazy("todo:tag-list")


class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("todo:tag-list")


class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy("todo:tag-list")
