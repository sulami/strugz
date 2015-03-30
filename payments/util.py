from braintree.error_result import ErrorResult

from notdienste.settings import PAYMENT_BACKEND

def create_payment(user, nonce):
    """Create a payment and return success (hopefully)"""

    pm = PAYMENT_BACKEND.create_payment_method(user, nonce)

    if isinstance(pm, ErrorResult):
        return False

    tr = PAYMENT_BACKEND.create_transaction('10.00', pm.payment_method.token)
    result = PAYMENT_BACKEND.submit_settlement(tr.transaction.id)

    return result.is_success

