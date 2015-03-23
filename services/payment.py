from payments.backends import BraintreeBackend

PAYMENT_BACKEND = BraintreeBackend()

def create_payment(user, nonce):
    """Create a payment and return success (hopefully)"""

    pm = PAYMENT_BACKEND.create_payment_method(user, nonce)
    tr = PAYMENT_BACKEND.create_transaction('10.00', pm.payment_method.token)
    result = PAYMENT_BACKEND.submit_settlement(tr.transaction.id)

    return result.is_success

