import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from .models import User
from .form import UserAddForm, UserUpdateForm
from .utils import ServerUserManager, Bash

CONNECTPY_PATH = os.path.join(settings.BASE_DIR, 'init.sh')


def user_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('users:list'))
            else:
                error = '用户以禁用'
        else:
            error = '用户名密码不正确'
    return render(request, 'users/login.html', {'error': error})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required(login_url=reverse_lazy('users:login'))
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
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user_in_server = ServerUserManager(Bash)
        ret, msg = user_in_server.present(username=username,
                                          password=password,
                                          shell=CONNECTPY_PATH)

        if not ret:
            user.save()
            return HttpResponseRedirect(reverse('users:list'))
        else:
            ret, msg = user_in_server.absent(username)
            return HttpResponse(msg)
    else:
        error = form.errors
        return HttpResponse('验证失败: {}'.format(error))


@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            if password:
                user.set_password(password)
                user_in_server = ServerUserManager(Bash)
                ret, msg = user_in_server.present(username=user.username, password=password)
                if ret:
                    return HttpResponse(msg)
            user.save()
            return HttpResponseRedirect(reverse('users:list'))
    form = UserUpdateForm(instance=user)
    return render(request, 'users/update.html', {'form': form})


@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(User, id=pk)
    return render(request, 'users/detail.html', {'user': user})


@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
def user_del(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return HttpResponse('删除成功')
