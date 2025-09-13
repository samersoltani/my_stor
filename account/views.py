from django.shortcuts import render, redirect
from django.contrib.auth import login ,logout , authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.views import View
from .models import CustomUser
from .forms import CustomUserCreationForm ,UserUpdateForm
from django.views.generic import TemplateView ,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin




def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: # تغییر اصلی: بررسی اینکه کاربر None نباشد
            login(request, user)
            # می‌توانید یک پیام موفقیت‌آمیز هم اینجا اضافه کنید
            # messages.success(request, f'خوش آمدید {username}!')
            return redirect('core:home') # یا هر صفحه‌ای که می‌خواهید کاربر بعد از لاگین به آنجا برود
        else:
            messages.error(request, 'نام کاربری یا رمز عبور نادرست است')
            # نیازی به return redirect یا render جداگانه در این else نیست،
            # چون در نهایت به render اصلی در انتهای تابع می‌رسد.
    return render(request, 'account/login.html')



class RegisterView(CreateView):
    form_class = CustomUserCreationForm  #فرم سفارشی 
    template_name = 'account/register.html'
    success_url = reverse_lazy('core:home') # این خط کاملا درست است

    def form_valid(self, form):
        # اول، اجازه می‌دهیم متد والد کار خودش را بکند (کاربر را بسازد و پاسخ ریدایرکت را آماده کند)
        response = super().form_valid(form)
        
        # کاربر جدید ساخته شده در self.object ذخیره می‌شود
        user = self.object
        
        # کاربر را بلافاصله پس از ثبت‌نام لاگین می‌کنیم
        login(self.request, user)
        
        # در نهایت، پاسخی که در خط اول آماده شده بود را برمی‌گردانیم تا ریدایرکت انجام شود
        return response
    


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج شدید')
        return redirect('core:home')
    

  
class ProfileView(LoginRequiredMixin,TemplateView):
            template_name = 'account/profile.html'
            login_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    form_class = UserUpdateForm 
    template_name = 'account/profile_edit.html'
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user 
    
    
    def form_valid(self, form):
        messages.success(self.request ,'پروفایل شما با موفقیت به‌روزرسانی شد')
        return super().form_valid(form)
    