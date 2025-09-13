from django import forms 
from .models import Review


 


class ReviewForm(forms.ModelForm):
    class Meta :
        model = Review 
        fields = ['rating' ,'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control','rows': 4,'placeholder': 'نظر خود را بنویسید...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control','min': 1,'max': 5,
                'style': 'width: 80px;'
            })
        }
        
        labels = {
            'rating': 'امتیاز شما (۱ تا ۵)',
            'comment': 'متن نظر'
        }


class CouponApplyForm(forms.Form):
    code = forms.CharField(label ='کد تخفیف')
    


class ContactForm(forms.Form):
    """
    فرم تماس با ما برای دریافت پیام از کاربران.
    """
    name = forms.CharField(max_length=100,label="نام شما",widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="ایمیل شما",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, label="موضوع",widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="پیام شما",widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))