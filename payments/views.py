from django.shortcuts import render, redirect

from notdienste.settings import PAYMENT_BACKEND
from payments.util import create_payment

def payment(request):
    context = {
        'token': PAYMENT_BACKEND.get_client_token(request.user),
    }

    return render(request, 'payments/payment.html', context)

def checkout(request):
    if request.method != 'POST':
        return redirect('/')

    if create_payment(request.user, request.POST.get('payment_method_nonce')):
        return render(request, 'payments/payment_complete.html')
    else:
        return render(request, 'payments/payment_failed.html')


