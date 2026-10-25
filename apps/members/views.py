from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .forms import MemberForm


def staff_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return wrapper


@staff_required
def users_index(request):
    users = User.objects.order_by('username')
    return render(request, 'users_index.html', {'users': users})


@staff_required
def create_user(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, creating=True, can_manage_staff=request.user.is_superuser)
        if form.is_valid():
            form.save()
            messages.success(request, _('User created successfully.'))
            return redirect('users_index')
    else:
        form = MemberForm(creating=True, can_manage_staff=request.user.is_superuser)

    return render(request, 'user_form.html', {'form': form, 'creating': True})


@staff_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=user, can_manage_staff=request.user.is_superuser)
        if form.is_valid():
            if user == request.user and not form.cleaned_data.get('is_active'):
                form.add_error('is_active', _('You cannot deactivate your own account.'))
            else:
                form.save()
                messages.success(request, _('User updated successfully.'))
                return redirect('users_index')
    else:
        form = MemberForm(instance=user, can_manage_staff=request.user.is_superuser)

    return render(request, 'user_form.html', {'form': form, 'user': user, 'creating': False})


@staff_required
@require_POST
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, _('You cannot delete your own account.'))
        return redirect('users_index')

    if user.is_superuser:
        if not request.user.is_superuser:
            raise PermissionDenied
        if User.objects.filter(is_superuser=True).count() <= 1:
            messages.error(request, _('The last superuser cannot be deleted.'))
            return redirect('users_index')

    user.delete()
    messages.success(request, _('User deleted successfully.'))
    return redirect('users_index')
