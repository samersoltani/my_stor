from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
import json

#? بررسی حالت سندباکس (تستی) یا واقعی
if settings.ZARINPAL_CONFIG['SANDBOX']:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# آدرس‌های REST API زرین‌پال
# توجه: این آدرس‌ها طبق نمونه کد شما برای نسخه REST است، نه SOAP
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# ===== تابع ارسال به درگاه (اصلاح شده) =====
def zarinpal_send_request(request, amount, description):
    # این تابع حالا مبلغ و توضیحات را به عنوان ورودی می‌گیرد
    
    # آدرس بازگشت را اینجا تعریف می‌کنیم
    CallbackURL = request.build_absolute_uri('/payment/verify/')

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "description": description,
        "callback_url": CallbackURL,
        "currency": "IRT", # واحد پول: تومان
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['code'] == 100:
                # اگر موفق بود، آدرس صفحه پرداخت و authority را برمی‌گردانیم
                startpay_url = ZP_API_STARTPAY + response_json['data']['authority']
                return {'status': True, 'url': startpay_url}
            else:
                # اگر خطایی از زرین‌پال آمد
                return {'status': False, 'code': response_json['errors']['code'], 'message': response_json['errors']['message']}
        
        return {'status': False, 'code': response.status_code, 'message': 'خطا در دریافت پاسخ از سرور'}

    except requests.exceptions.RequestException as e:
        return {'status': False, 'code': 'network_error', 'message': str(e)}


# ===== تابع تایید پرداخت (اصلاح شده) =====
def zarinpal_verify(amount, authority):
    # این تابع حالا مبلغ را به عنوان ورودی می‌گیرد
    data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['code'] == 100:
                # پرداخت موفق
                return {'status': True, 'ref_id': response_json['data']['ref_id']}
            else:
                # پرداخت ناموفق یا خطا
                return {'status': False, 'code': response_json['errors']['code'], 'message': response_json['errors']['message']}
        
        return {'status': False, 'code': response.status_code, 'message': 'خطا در دریافت پاسخ از سرور'}
    
    except requests.exceptions.RequestException as e:
        return {'status': False, 'code': 'network_error', 'message': str(e)}


# این دو ویو را هم اضافه می‌کنیم تا با urls.py شما هماهنگ باشد، اما از آنها مستقیم استفاده نمی‌کنیم
def request(request):
    # این ویو صرفا برای تست مستقیم است و در پروژه اصلی استفاده نمی‌شود
    return HttpResponse("این صفحه برای تست مستقیم است. لطفا از طریق سبد خرید اقدام کنید.")

def verify(request):
    # این ویو هم در مرحله بعد توسط ویوی اصلی ما صدا زده می‌شود
    return HttpResponse("در حال تایید پرداخت...")

