from django.db import models
from django.urls import reverse
from django.conf import settings 
from django.core.validators import MinValueValidator, MaxValueValidator
 

class Category(models.Model):
    name = models.CharField(max_length=200 , db_index=True)
    slug =models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product_list_category',args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product',on_delete=models.CASCADE)
    name = models.CharField(max_length=200 ,db_index=True)
    slug = models.SlugField(max_length=200 ,db_index=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description= models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0,verbose_name='موجودی انبار')
    is_active = models.BooleanField(default=True ,verbose_name='فعال/موجود')

    class Meta:
        ordering = ('name',)
       

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product_detail', kwargs={'pk': self.pk})

    


class ProductImage(models.Model):
    # هر عکس به یک محصول مرتبط است
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    # فیلد خود عکس
    image = models.ImageField(upload_to='products/', blank=True, null=True)
       
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصول'

    def __str__(self):
        return f"تصویر برای {self.product.name}"
    
    # def get_absolute_url(self):
    #     # اضافه کردن پیشوند 'core:' به نام URL
    #     return reverse('core:product_detail', args=[self.id])
    def get_absolute_url(self):
        return reverse('core:product_detail', args=[self.product.id])
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class Review(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='محصول'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    ) 
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='پاسخ به'
    )
    comment = models.TextField(verbose_name='متن نظر')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="امتیاز بین ۱ تا ۵",
        null=True, 
        blank=True,
        verbose_name='امتیاز'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    is_approved = models.BooleanField(default=False, verbose_name='تایید شده')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        if self.parent:
            return f"پاسخ از {self.user} به نظر شماره {self.parent.id}"
        return f"نظر از {self.user} برای {self.product.name}"

    

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # هر کاربر فقط یک بار می‌تواند یک محصول را به لیست اضافه کند
        unique_together = ('user', 'product')
        ordering = ['-created_at']
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'

    def __str__(self):
        return f"{self.user.username} علاقه‌مند به {self.product.name}"  
    


class Order(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    total_paid =models.DecimalField(max_digits=10,decimal_places=2,default=0)

    
    class Meta:
        ordering = ('-created_at',)  # این برای ترتیب‌دهی است
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'


    def __str__(self):
        return f'سفارش{self.id}'

  # داخل کلاس Order
def get_total_cost(self):
    return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE ,related_name='items')
    product =models.ForeignKey(Product ,on_delete=models.CASCADE ,related_name='order_items')
    price =models.DecimalField(max_digits=10, decimal_places=2)
    quantity =models.PositiveBigIntegerField(default=1)


    class Meta:
        verbose_name = ('ایتم سفارش')
        verbose_name_plural = ('ایتم های سفارش')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True , verbose_name='کد تخفیف') 
    valid_from = models.DateTimeField(verbose_name='معتبر از تاریخ')
    valid_to = models.DateTimeField(verbose_name='معتبر تا تاریخ')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
    verbose_name='درصد تخفیف',help_text='عددی بین 0 تا 100 وارد کنید')
    active =models.BooleanField(default=True ,verbose_name='فعال')


    class Meta :
        verbose_name ='کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return self.code

