from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Product # فرض می‌کنیم مدل محصول شما در اپ core قرار دارد
from .cart import Cart # این کلاس را در قدم بعدی خواهیم ساخت
from core.forms import CouponApplyForm


@require_POST # این دکوراتور تضمین می‌کند که این ویو فقط با متد POST قابل دسترسی است
def add_to_cart(request, product_id):
    cart = Cart(request) # یک نمونه از کلاس سبد خرید می‌سازیم
    product = get_object_or_404(Product, id=product_id)
    
    # در اینجا می‌توانید یک فرم برای گرفتن تعداد هم داشته باشید، فعلا ساده کار می‌کنیم
    cart.add(product=product, quantity=1) # محصول را به سبد اضافه می‌کنیم
    
    return redirect('cart:cart_detail') # کاربر را به صفحه سبد خرید منتقل می‌کنیم


def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm() # یک نمونه از فرم می‌سازیم
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form # فرم را به تمپلیت پاس می‌دهیم
    })



def cart_remove(request ,product_id):
    cart =Cart(request)
    product =get_object_or_404(Product ,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
