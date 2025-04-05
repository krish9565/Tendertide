from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser

# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             next_url = request.GET.get('next')
#             return redirect(next_url or 'tenders:home')
#         messages.error(request, 'Invalid email or password.')
#     return render(request, 'login.html')
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'login.html')

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') or 'tenders:home')
        else:
            messages.error(request, 'Incorrect password.')

    return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type', 'user')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        company_name = request.POST.get('company_name') if account_type == 'company' else None

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('accounts:register')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            account_type=account_type,
            company_name=company_name
        )
        login(request, user)
        return redirect('tenders:home')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('tenders:home')

@login_required
def profile_view(request):
    if request.user.is_company():
        return redirect('accounts:company_profile')
    
    return render(request, 'profile_user.html', {
        'current_user': request.user,  # Add this line to pass current_user
        'favorite_tenders': request.user.favorite_tenders.all()
    })


@login_required
def company_profile_view(request):
    if not request.user.is_company():
        return redirect('accounts:profile')
    return render(request, 'company_profile.html', {
        'published_tenders': request.user.tender_set.all()
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard_view(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        if not user.is_superuser:
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User {user.username} {status} successfully.')
    return redirect('accounts:admin_dashboard')
