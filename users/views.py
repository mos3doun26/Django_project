from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserResigterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = UserResigterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Your account has been created, Login Now!")
            return redirect("login")
    else:
        form = UserResigterForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST": 
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES, instance=request.user.profile)
    context={
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "users/profile.html", context)

def costume_logout(request):
    logout(request)
    return redirect("login")
