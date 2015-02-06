import braintree

class BraintreeBackend:
    """Backend to interact with Braintree Payments"""

    def __init__(self):
        """Configure the Braintree connection"""
        braintree.Configuration.configure(braintree.Environment.Sandbox,
                            merchant_id='gqg3fj2qdfrdd5bf',
                            public_key='n6nz46v52p6d368x',
                            private_key='f7bf15fb7a68359e0b82a41d4ca96df8')

    def get_client_token(self, user):
        """Get a token for the client's Braintree interaction"""
        return braintree.ClientToken.generate({ 'customer_id': user.pk })

    def create_customer(self, User):
        """Create a customer at Braintree and return the id"""
        result = braintree.Customer.create({
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        if result.is_success:
            return result.customer.id
        else:
            raise Exception('Could not create customer')

    def create_payment_method(self, user, nonce):
        """Pass customer payment information to the Braintree Vault"""
        return braintree.PaymentMethod.create({
            'customer_id': str(user.pk),
            'payment_method_nonce': nonce,
        })

    def create_transaction(self, amount, token):
        return braintree.Transaction.sale({
            'amount': amount,
            'payment_method_token': token,
        })

