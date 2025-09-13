from decimal import Decimal
from django.conf import settings
from core.models import Product, Coupon # مدل‌های Product و Coupon را ایمپورت می‌کنیم

class Cart:
    def __init__(self, request):
        """
        مقداردهی اولیه سبد خرید
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # اگر سبد خریدی در سشن نبود، یک سبد خرید خالی می‌سازیم
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
        # --- بخش جدید: ذخیره کد تخفیف اعمال شده ---
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
        افزودن محصول به سبد خرید یا به‌روزرسانی تعداد آن
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # علامت‌گذاری سشن به عنوان "تغییر یافته" برای اطمینان از ذخیره شدن آن
        self.session.modified = True

    def remove(self, product):
        """
        حذف یک محصول از سبد خرید
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        ایجاد یک حلقه روی آیتم‌های سبد خرید و گرفتن محصولات از پایگاه داده
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        محاسبه تعداد کل آیتم‌ها در سبد خرید
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        محاسبه قیمت کل سبد خرید
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # حذف سبد خرید از سشن
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # =========================================================
    # === متدهای جدید برای کار با کد تخفیف (مهم) ===
    # =========================================================
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()