from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('organization/signup/', views.organization_signup, name='organization_signup'),
    path('organization/login/', views.organization_login, name='organization_login'),
    path('worker/signup/', views.worker_signup, name='worker_signup'),
    path('worker/login/', views.worker_login, name='worker_login'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('community-board/<str:work_address>/', views.community_board, name='community_board'),
   path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
