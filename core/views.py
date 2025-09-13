from django.shortcuts import get_object_or_404 ,redirect ,render
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, CreateView, ListView ,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category, Review  ,Wishlist
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST 
from django.db.models import Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem ,Coupon
from cart.cart import Cart 
from django.views.generic import DetailView 
from django.utils import timezone
from .forms import CouponApplyForm ,ContactForm
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render



class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ... (کدهای قبلی شما برای محصولات ویژه و ...) ...
        context['featured_products'] = Product.objects.filter(available=True, is_featured=True).order_by('-created_at')[:3]
        context['products'] = Product.objects.filter(available=True).annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        # ... (بقیه context های شما) ...

        # === بخش جدید: اضافه کردن آخرین نظرات تایید شده ===
        context['latest_reviews'] = Review.objects.filter(
            is_approved=True, 
            parent__isnull=True  # فقط نظرات اصلی (نه پاسخ‌ها)
        ).select_related('user', 'product').order_by('-created_at')[:3] # 3 نظر آخر

        if self.request.user.is_authenticated:
            context['wishlist_ids'] = Wishlist.objects.filter(user=self.request.user).values_list('product__id', flat=True)
        else:
            context['wishlist_ids'] = []

        return context



class ProductDetailView(DetailView):
    model = Product
    # نام تمپلیت را به product_detail.html تغییر می‌دهیم
    template_name = 'core/product_detail.html'
    context_object_name = 'product'
    # ما از pk در URL استفاده می‌کنیم، پس نیازی به slug_url_kwarg نیست

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # نظرات اصلی (بدون والد) را فیلتر می‌کنیم
        context['reviews'] = product.reviews.filter(is_approved=True, parent__isnull=True)
        context['review_form'] = ReviewForm()

        # منطق لیست علاقه‌مندی‌ها
        if self.request.user.is_authenticated:
            context['wishlist_ids'] = Wishlist.objects.filter(user=self.request.user).values_list('product__id', flat=True)
        else:
            context['wishlist_ids'] = []
            
        return context


class AboutView(TemplateView):
    """
    ویو برای نمایش صفحه درباره ما
    """
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- شروع کد موقت برای ساخت ادمین ---
        User = get_user_model()
        try:
            # نام کاربری که با آن ثبت‌نام کردید را اینجا بنویسید
            user = User.objects.get(username='Samer_Admin')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"موفقیت: کاربر {user.username} به ادمین تبدیل شد.")
            context['promotion_message'] = f"کاربر {user.username} با موفقیت به ادمین تبدیل شد."
        except ObjectDoesNotExist:
            print("خطا: کاربر پیدا نشد.")
            context['promotion_message'] = "کاربر مورد نظر برای ارتقا پیدا نشد."
        # --- پایان کد موقت ---
        
        return context

    """
    ویو برای نمایش صفحه تماس با ما
    """
class ContactView(View):
    template_name = 'core/contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        """
        درخواست GET: یک فرم خالی را نمایش می‌دهد.
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        درخواست POST: فرم ارسال شده را پردازش می‌کند.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email'] # نام متغیر را تغییر دادم تا با ایمیل جنگو تداخل نداشته باشد
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message'] # نام متغیر را تغییر دادم

            # آماده‌سازی و ارسال ایمیل
            full_subject = f'پیام جدید از سایت: {subject}'
            full_message = f'نام فرستنده: {name}\nایمیل فرستنده: {from_email}\n\nمتن پیام:\n{message_body}'
            
            try:
                send_mail(
                    subject=full_subject,
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                # === استفاده صحیح از messages (جمع) ===
                messages.success(request, 'پیام شما با موفقیت ارسال شد. از تماس شما سپاسگزاریم!')
            except Exception as e:
                messages.error(request, 'خطایی در ارسال پیام رخ داد. لطفاً بعداً دوباره تلاش کنید.')
                print(f"Email sending error: {e}")

            return redirect('core:contact')

        # اگر فرم معتبر نبود
        # === استفاده صحیح از messages (جمع) ===
        messages.error(request, 'اطلاعات وارد شده صحیح نیست. لطفاً موارد مشخص شده را اصلاح کنید.')
        return render(request, self.template_name, {'form': form})



class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html' # این تمپلیت دیگر مستقیما استفاده نمی‌شود
    login_url = 'login'

    def form_valid(self, form):
        # پیدا کردن محصول
        self.product = get_object_or_404(Product, id=self.kwargs['product_id'])
        
        # اختصاص کاربر و محصول به نظر جدید
        form.instance.user = self.request.user
        form.instance.product = self.product
        
        # === بررسی وجود پاسخ ===
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            try:
                parent_review = Review.objects.get(id=parent_id)
                form.instance.parent = parent_review
                # برای پاسخ‌ها امتیاز در نظر نمی‌گیریم
                # form.instance.rating = 1# یا هر مقدار پیش‌فرض دیگر
            except Review.DoesNotExist:
                form.instance.parent = None
        # =======================

        messages.success(self.request, 'نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد.')
        return super().form_valid(form)
    
    def get_success_url(self):
        # بازگشت به همان صفحه جزئیات محصول
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return product.get_absolute_url()
    
def form_invalid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        # اضافه کردن پیام خطا برای کاربر
        messages.error(self.request, 'اطلاعات وارد شده صحیح نیست. لطفاً تمام فیلدها را بررسی کنید.')
        # برای اینکه کاربر در همان صفحه بماند و خطای فرم را ببیند،
        # به جای ریدایرکت، می‌توانیم صفحه را دوباره رندر کنیم.
        # اما برای سادگی، فعلا ریدایرکت می‌کنیم.
        return redirect(product.get_absolute_url())


class ProductListView(ListView):
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.filter(available=True).annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated :
            context['wishlist_ids'] = Wishlist.objects.filter(user=self.request.user).values_list('product__id', flat=True)
        else:
            context['wishlist_ids'] = []         
        return context


class CategoryProductView(ListView):
    template_name = 'core/product_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(
            category=self.category, 
            available=True
        ).annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category

        if self.request.user.is_authenticated :
            context['wishlist_ids'] = Wishlist.objects.filter(user=self.request.user).values_list('product__id', flat=True)
        else :
            context['wishlist_ids'] = []


        return context



class ProductSearchView(ListView):
    template_name = 'core/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                name__icontains=query, 
                available=True
            )
        return Product.objects.none()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wishlist_ids'] = Wishlist.objects.filter(user=self.request.user).values_list('product__id',flat=True)
        else:
            context['wishlist_ids'] = []
        context['query'] = self.request.GET.get('q','')
        return context    


class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'core/wishlist.html'
    login_url = 'login' # آدرس صفحه لاگین شما

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # فقط آیتم‌هایی که توسط کاربر فعلی لایک شده را نمایش بده
        context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user)
        return context
    

@require_POST
@login_required(login_url='login')
def toggle_wishlist(request, product_id):

    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            action = 'removed'
            message = f'"{product.name}"از علاقه‌مندی‌ها حذف شد'
        else:
            action = 'added'
            message = f'"{product.name}"به علاقه‌مندی‌ها اضافه شد'
        
        # با حذف آن شرط، دیگر نیازی به ارسال هدر X-Requested-With از سمت جاوا اسکریپت هم نیست
        return JsonResponse({'status': 'ok', 'action': action, 'message': message})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/account_dashboard.html'
    login_url = 'login'


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context 
    
class orderHistoryView(LoginRequiredMixin ,ListView):
    model = Order
    template_name ='core/order_history.html'
    context_object_name ='orders'
    login_url = 'login'

    def get_queryset(self):
        # فقط سفارش‌های کاربر لاگین کرده را برمی‌گردانیم
        return Order.objects.filter(user=self.request.user)


@login_required
def create_test_order(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('core:home')

    # ایجاد سفارش اصلی
    order = Order.objects.create(user=request.user, is_paid=False) # به صورت تستی پرداخت شده در نظر میگیریم
    total_cost = 0

    # ایجاد آیتم‌های سفارش از روی سبد خرید
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
        total_cost += item['price'] * item['quantity']
    
    order.total_paid = total_cost
    order.save()
    
    # خالی کردن سبد خرید
    cart.clear()

    messages.success(request, 'سفارش تستی شما با موفقیت ایجاد شد!')
    return redirect('core:order_history') # کاربر را به صفحه تاریخچه سفارش‌ها هدایت میکنیم


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
    login_url = 'login'

    def get_queryset(self):
        # *** نکته امنیتی بسیار مهم ***
        # این متد تضمین می‌کند که کاربر فقط به سفارش‌های خودش دسترسی دارد.
        # اگر کاربر دیگری شماره سفارش را در URL حدس بزند، با خطای 404 مواجه می‌شود.
        return Order.objects.filter(user=self.request.user)
    

# ===============================================
# === ویو برای اعمال کردن کد تخفیف روی سبد خرید ===
# ===============================================
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,      # جستجوی بدون حساسیت به بزرگی و کوچکی حروف
                valid_from__lte=now,    # تاریخ شروع اعتبار گذشته باشد
                valid_to__gte=now,      # تاریخ پایان اعتبار فرا نرسیده باشد
                active=True
            )
            # اگر کد معتبر بود، ID آن را در سشن کاربر ذخیره می‌کنیم
            request.session['coupon_id'] = coupon.id
            messages.success(request, 'کد تخفیف با موفقیت اعمال شد.')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None # اگر کد نامعتبر بود، سشن را پاک می‌کنیم
            messages.error(request, 'کد تخفیف وارد شده معتبر نیست.')

    # کاربر را به همان صفحه سبد خرید برمی‌گردانیم
    return redirect('cart:cart_detail') # فرض می‌کنیم URL سبد خرید شما این است


from zarinpal.views import zarinpal_send_request, zarinpal_verify

# این کد با دستورات print برای عیب‌یابی است
@login_required
def send_to_payment_gateway(request, order_id):
    print("\n--- مرحله ۱: وارد ویو send_to_payment_gateway شدیم. ---")
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_paid:
        print("--- مرحله ۲ (خطا): سفارش قبلاً پرداخت شده است. ---")
        messages.error(request, 'این سفارش قبلاً پرداخت شده است.')
        return redirect('core:order_detail', pk=order.id)

    # استفاده از توابع کمکی که در zarinpal/views.py ساختیم
    from zarinpal.views import zarinpal_send_request
    
    amount = int(order.total_paid)
    description = f"پرداخت برای سفارش شماره {order.id}"
    
    print(f"--- مرحله ۳: در حال فراخوانی تابع zarinpal_send_request با مبلغ {amount} و توضیحات: '{description}' ---")
    
    # فراخوانی تابع کمکی از جعبه ابزار زرین‌پال
    response_data = zarinpal_send_request(request, amount, description)

    # این مهم‌ترین بخش برای دیباگ است
    print(f"--- مرحله ۴: نتیجه بازگشتی از تابع کمکی: {response_data} ---")

    if response_data['status']:
        # اگر درخواست موفق بود
        request.session['order_id_to_verify'] = order.id
        print("--- مرحله ۵ (موفقیت): در حال هدایت به آدرس:", response_data['url'], "---")
        return redirect(response_data['url'])
    else:
        # اگر خطایی رخ داد
        error_message = response_data.get('message', 'خطای نامشخص')
        print(f"--- مرحله ۶ (خطا): پیام خطا: {error_message} ---")
        messages.error(request, error_message)
        return redirect('core:order_detail', pk=order.id)


def payment_verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    # ID سفارشی که قبل از پرداخت در سشن ذخیره کردیم را می‌خوانیم
    order_id = request.session.get('order_id_to_verify')

    if not order_id:
        messages.error(request, 'فرآیند پرداخت با مشکل مواجه شد (سفارش پیدا نشد).')
        return redirect('core:home')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'سفارش شما در سیستم پیدا نشد.')
        return redirect('core:home')
    
    amount = int(order.total_paid)

    if status == 'OK':
        # اگر کاربر پرداخت را با موفقیت انجام داده بود
        # حالا باید تراکنش را با زرین‌پال تایید نهایی کنیم
        from zarinpal.views import zarinpal_verify # ایمپورت تابع کمکی
        response_data = zarinpal_verify(amount, authority)

        if response_data['status']:
            # اگر تایید نهایی هم موفق بود
            order.is_paid = True
            # می‌توانید کد رهگیری را هم در مدل Order ذخیره کنید (اختیاری)
            # order.ref_id = response_data['ref_id']
            order.save()
            
            # پاک کردن ID سفارش از سشن
            if 'order_id_to_verify' in request.session:
                del request.session['order_id_to_verify']

            messages.success(request, f"پرداخت شما با موفقیت انجام شد. کد رهگیری: {response_data['ref_id']}")
            return redirect('core:order_detail', pk=order.id)
        else:
            # اگر تایید نهایی ناموفق بود
            messages.error(request, response_data['message'])
            return redirect('core:order_detail', pk=order.id)
    else:
        # اگر کاربر از پرداخت انصراف داده باشد
        messages.warning(request, 'شما از ادامه فرآیند پرداخت انصراف دادید.')
        return redirect('core:order_detail', pk=order.id)

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, 'سبد خرید شما برای تسویه حساب خالی است.')
        return redirect('core:home')

    # مرحله ۱: ایجاد سفارش دائمی از روی سبد خرید
    order = Order.objects.create(user=request.user)
    total_cost = 0

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
        total_cost += item['price'] * item['quantity']
    
    order.total_paid = total_cost
    order.save()
    
    # خالی کردن سبد خرید بعد از ثبت سفارش
    cart.clear()

    # مرحله ۲: هدایت کاربر به درگاه پرداخت برای سفارش جدید
    # ما کاربر را به همان ویوی قبلی (send_to_payment_gateway) می‌فرستیم
    messages.success(request, 'سفارش شما با موفقیت ثبت شد. در حال انتقال به درگاه پرداخت...')
    return redirect('core:pay_for_order', order_id=order.id)