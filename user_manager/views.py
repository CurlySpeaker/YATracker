from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
)

from django.contrib.auth import update_session_auth_hash
from user_manager.forms import PasswordChangeForm
from django.shortcuts import render

from django.contrib.auth import get_user_model
User = get_user_model()


def require_authorized(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return function(request, *args, **kwargs)
    return wrapper


@require_authorized
def personal(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, 'user_manager/account.html', {'user': user})


@require_authorized
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            old_pass = form.cleaned_data['old_password']
            new_pass = form.cleaned_data['new_password']
            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                return personal(request)
    else:
        form = PasswordChangeForm()
    return render(request, 'user_manager/change_password.html', {'form': form})
