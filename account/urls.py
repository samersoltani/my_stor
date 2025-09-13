from django.urls import path , reverse_lazy
from.import views 
from.views import RegisterView,CustomLogoutView ,ProfileView,ProfileUpdateView
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',RegisterView.as_view(),name='register' ),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', ProfileUpdateView.as_view(), name='profile_edit'),
    path('password-change/', 
        auth_views.PasswordChangeView.as_view(
             template_name='account/password_change.html',
             success_url=reverse_lazy('password_change_done')),name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),

]