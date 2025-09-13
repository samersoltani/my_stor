from django.urls import path
from . import views 
from .views import (HomeView, ReviewCreateView,ProductListView,
                    CategoryProductView,ProductSearchView,WishlistView,
                    ProductDetailView ,AccountDashboardView ,orderHistoryView,
                    OrderDetailView,AboutView,ContactView)



app_name = 'core'
 
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', CategoryProductView.as_view(), name='product_list_category'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    path('products/<int:product_id>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('wishlist/',WishlistView.as_view(), name='wishlist_detail'),
    path('wishlist/toggle/<int:product_id>/',views.toggle_wishlist, name='toggle_wishlist'),
    path('account/',AccountDashboardView.as_view(),name='account_dashboard'),
    path('account/orders/',orderHistoryView.as_view(), name='order_history'),
    path('account/orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    # --- URL تستی برای ایجاد سفارش ---
    path('create-test-order/', views.create_test_order, name='create_test_order'),
    path('apply_coupon/',views.coupon_apply,name='coupon_apply'),
    path('pay/<int:order_id>/', views.send_to_payment_gateway, name='pay_for_order'),
    # --- URL جدید برای بازگشت از درگاه ---
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    path('checkout/', views.checkout, name='checkout'),
     # === بخش جدید: آدرس برای صفحات جدید ===
    path('about-us/', AboutView.as_view(), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
]
