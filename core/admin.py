from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Wishlist, Coupon, OrderItem, Order

# Inline برای نمایش تصاویر گالری در صفحه محصول
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # تعداد فرم خالی برای آپلود تصویر جدید
    # این فیلدها را اضافه می‌کنیم تا مطمئن شویم ادمین به درستی کار می‌کند
    fields = ('image',) 
    
# Inline برای نمایش آیتم‌های سفارش در صفحه سفارش
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # خطای تایپی در اینجا اصلاح شد
    raw_id_fields = ['product'] 
    readonly_fields = ['product', 'price', 'quantity']
    extra = 0  # برای جلوگیری از نمایش فرم خالی

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'stock', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    list_editable = ('is_approved',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ['user', 'product']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_paid', 'total_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['id', 'user__username']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'

