from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from core.models import Product # فرض می‌کنیم مدل محصول شما در اپ core قرار دارد
from .cart import Cart # این کلاس را در قدم بعدی خواهیم ساخت
from core.forms import CouponApplyForm


@require_POST # این دکوراتور تضمین می‌کند که این ویو فقط با متد POST قابل دسترسی است
def add_to_cart(request, product_id):
    cart = Cart(request) # یک نمونه از کلاس سبد خرید می‌سازیم
    product = get_object_or_404(Product, id=product_id)
    
    try:
        # دریافت تعداد از POST یا استفاده از مقدار پیش‌فرض
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'{product.name} به سبد خرید اضافه شد.')
    except ValueError as e:
        messages.error(request, str(e))
    
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
