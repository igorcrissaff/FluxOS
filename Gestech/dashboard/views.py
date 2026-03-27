from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

    if request.method == 'GET':
        user = request.user
        form = UserChangeForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'form': form})

