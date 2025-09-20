import stripe
from django.conf import settings
from decimal import Decimal

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency='usd', metadata=None):
    """
    Create a Stripe PaymentIntent for donation processing
    """
    try:
        # Convert amount to cents (Stripe uses smallest currency unit)
        amount_cents = int(float(amount) * 100)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={
                'enabled': True,
            },
        )
        
        return {
            'success': True,
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id
        }
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }

def confirm_payment_intent(payment_intent_id):
    """
    Confirm a payment intent after successful payment
    """
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'success': True,
            'payment_intent': payment_intent
        }
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }
