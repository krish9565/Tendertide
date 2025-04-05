from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('company/profile/', views.company_profile_view, name='company_profile'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('user/<int:pk>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
]
