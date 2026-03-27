from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
@login_required
def users_index(request):
    users = User.objects.all()
    return render(request, 'users_index.html', {'users': users})

@login_required
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(users_index, permanent=True)
        
        else:
            return render(request, 'user_form.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'user_form.html', {'form': form})

def edit_user(request, user_id):
    raise NotImplementedError("Edit user functionality is not implemented yet.")

def delete_user(request, user_id):
    raise NotImplementedError("Delete user functionality is not implemented yet.")