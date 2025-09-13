from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # فیلد عکس پروفایل با یک مقدار پیش‌فرض مناسب
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        default='profile_images/default-avatar.png', # یک عکس پیش‌فرض در این مسیر قرار دهید
        verbose_name='تصویر پروفایل'
    )

    # related_name ها برای جلوگیری از تداخل با مدل پیش‌فرض User ضروری هستند
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='گروه‌ها',
        blank=True,
        help_text='گروه‌هایی که این کاربر به آن‌ها تعلق دارد.',
        related_name="customuser_set_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='دسترسی‌های کاربر',
        blank=True,
        help_text='دسترسی‌های خاص برای این کاربر.',
        related_name="customuser_set_permissions",
        related_query_name="user",
    )

    class Meta:
        verbose_name = 'کاربر سفارشی'
        verbose_name_plural = 'کاربران سفارشی'
        default_permissions = ()

    def __str__(self):
        return self.get_full_name() or self.username