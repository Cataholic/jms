from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .form import UserAddForm, UserUpdateForm


def user_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('users:user_list'))
        error = '用户名密码不正确'
    return render(request, 'users/login.html', {'error': error})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:user_login'))


@login_required(login_url=reverse_lazy('users:user_login'))
@user_passes_test(lambda user: user.is_superuser)
def user_list(request):
    users = User.objects.all()
    form = UserAddForm()
    return render(request, 'users/list.html', {'users': users, 'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def user_add(request):
    form = UserAddForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('users:list'))
    return HttpResponse('添加失败')


@login_required(login_url=reverse_lazy('users:user_login'))
@user_passes_test(lambda user: user.is_superuser)
def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:list'))
    form = UserUpdateForm(instance=user)
    return render(request, 'users/update.html', {'form': form})


@login_required(login_url=reverse_lazy('users:user_login'))
@user_passes_test(lambda user: user.is_superuser)
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/detail.html', {'user': user})


@login_required(login_url=reverse_lazy('users:user_login'))
@user_passes_test(lambda user: user.is_superuser)
def user_del(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return HttpResponse('删除成功')
