from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, profileUpdateForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('email')}")
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "users/register.html", context=context)


def login(request):
    return render(request, "users/login.html", context={})


def logout(request):
    return render(request, "users/logout.html", context={})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "users/profile.html", context=context)


def user_info(request, user_id, *args):
    user = User.objects.filter(id=user_id).first()
    user = {
        'Username': user.username,
        'ID': user.id,
        'Email': user.email,
        '18+': "Yes" if user.profile.plus18 else "No",
    }
    context = {'user_obj': user}
    return render(request, "users/user-info.html", context)

