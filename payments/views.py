from django.shortcuts import render, redirect, get_object_or_404

from notdienste.settings import PAYMENT_BACKEND, MONTHLY_PRIZE
from payments.models import Payment
from payments.util import create_payment
from services.models import User

def list(request):
    if not request.user.is_authenticated():
        return redirect('/')

    payments = Payment.objects.filter(user=request.user).order_by('-date')

    context = {
        'payments': payments,
    }

    return render(request, 'payments/list.html', context)

def bill(request, pid):
    if not request.user.is_authenticated():
        return redirect('/')

    payment = get_object_or_404(Payment, pk=pid)

    # TODO Generate a bill to print out.

    return render(request, 'services/bill.html')

def payment(request):
    context = {
        'token': PAYMENT_BACKEND.get_client_token(request.user),
    }

    return render(request, 'payments/payment.html', context)

def checkout(request):
    if request.method != 'POST':
        return redirect('/')

    if create_payment(request.user, request.POST.get('payment_method_nonce'),
        MONTHLY_PRIZE):
        p = Payment()
        p.yearly = False # This is a monthly payment.
        p.user = request.user
        p.amount = MONTHLY_PRIZE
        p.save()

        return render(request, 'payments/payment_complete.html')
    else:
        return render(request, 'payments/payment_failed.html')


