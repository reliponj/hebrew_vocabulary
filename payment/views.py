from datetime import timedelta

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from all_pay.api import AllPayAPI
from ivrit.models import Setting
from payment.models import Payment


def status(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'payment_status.html')


def create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    setting = Setting.get_settings()
    payment = Payment(
        user=request.user,
        sum=setting.payment_sum)
    payment.save()

    host = request.get_host()
    callback_url = f"https://{host}{reverse('pay_callback')}"
    url = AllPayAPI().create_payment(payment, callback_url)
    return redirect(url)


def trial(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_trial_used:
        return redirect('index')

    request.user.is_trial_used = True
    request.user.sub_date = timezone.now() + timedelta(days=30)
    request.user.is_subscribe = True
    request.user.save()
    return redirect('index')


def callback(request):
    if request.method != 'POST':
        return redirect('index')

    data = request.POST
    sign = AllPayAPI().get_sign(data)

    if sign != data['sign']:
        return redirect('index')

    payment = Payment.objects.filter(id=data['order_id']).first()
    user = payment.user
    if data['status'] == 1 and payment.status != 'success':
        payment.status = 'success'
        user.sub_date = timezone.now() + timedelta(days=30)
        user.is_subscribe = True
    elif data['status'] == 3 and payment.status != 'refund':
        payment.status = 'refund'
        user.sub_date = timezone.now() - timedelta(days=30)
        user.is_subscribe = False

    user.save()
    payment.save()
