from django.urls import reverse_lazy
from users.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Asset
from .form import AssetForm


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    context_object_name = 'assets'
    template_name = 'assets/list.html'


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/create.html'
    success_url = reverse_lazy('assets:list')


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'assets/detail.html'


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/update.html'
    success_url = reverse_lazy('assets:list')


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'assets/create.html'
    success_url = reverse_lazy('assets:list')
