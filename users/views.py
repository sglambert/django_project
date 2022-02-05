from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
	"""
	Functional view for user registration.
	"""
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid(): 
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Hi, {username}, your account was created login to continue!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	"""
	Functional view for profile updates.
	"""
	if request.method == 'POST':
		user_update_form = UserUpdateForm(request.POST, instance=request.user)
		profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if user_update_form.is_valid() and profile_update_form.is_valid():
			user_update_form.save()
			profile_update_form.save()
			messages.success(request, f'Account updated')
			return redirect('profile')
	else:
		user_update_form = UserUpdateForm(instance=request.user)
		profile_update_form = ProfileUpdateForm(instance=request.user.profile)
	context = {'u_form': user_update_form, 'p_form': profile_update_form}
	return render(request, 'users/profile.html', context)
