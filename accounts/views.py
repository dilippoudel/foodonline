from django.shortcuts import render, redirect
from accounts.utils import detectUser
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


def registerUser(request):
    """Create the user in the database."""
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using create_user method.
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,
                             'Your account has been registerd successfully!')
            return redirect('registerUser')
        else:
            messages.error(request, form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    """Create the vendor in the database from form."""
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('registerVendor')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create(first_name=first_name,
                                       last_name=last_name,
                                       username=username,
                                       email=email)
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,
                             'Your account has been registered sucessfully! \
                                 please wait for the approval.')
            return redirect('registerVendor')
        else:
            print(form.errors)

    form = UserForm()
    v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid log in credentials.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are successfully logged out.')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
