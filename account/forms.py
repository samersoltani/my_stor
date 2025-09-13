from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
    fields =UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'profile_image')
        



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ('first_name', 'last_name', 'email' , 'profile_image')


        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'lost_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            
              # این خط به جنگو می‌گوید که برای فیلد عکس، فقط یک دکمه آپلود ساده نمایش بده
            'profile_image': forms.FileInput(attrs={'class':'form-control'}),
        }
       