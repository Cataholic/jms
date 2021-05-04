from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import SingleObjectMixin
from django.views.generic import ListView, DetailView, CreateView, View
from .models import Perm
from users.mixins import LoginRequiredMixin
from .form import PermForm


class PermListView(LoginRequiredMixin, ListView):
    model = Perm
    template_name = 'perms/list.html'
    form = PermForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PermListView, self).get_context_data()
        context['form'] = self.form
        return context


class PermDetailView(LoginRequiredMixin, DetailView):
    model = Perm
    template_name = 'perms/detail.html'


class PermCreateView(LoginRequiredMixin, CreateView):
    model = Perm
    template_name = 'perms/create.html'
    success_url = reverse_lazy('perms:list')
    form_class = PermForm


class PermDeleteView(SingleObjectMixin, View):
    model = Perm

    def post(self, request, *args, **kwargs):
        perm = self.get_object()
        perm.delete()
        return HttpResponse("删除成功")
