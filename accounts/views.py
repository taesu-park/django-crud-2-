from IPython import embed
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) # 로그인!
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user) # 반드시 첫번째 인자로 user
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def profile(request, account_pk):
    # user = User.objects.get(pk=account_pk)
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk)
    context = {
        'user_profile': user
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User, pk=account_pk)
    if obama != request.user:
        # obama를 팔로우 한 적 있다면
        if request.user in obama.followers.all():
            # 취소
            obama.followers.remove(request.user)
        # 아니면
        else:
            obama.followers.add(request.user)
            # 팔로우
    return redirect('accounts:profile', account_pk)