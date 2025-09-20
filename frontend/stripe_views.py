from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import json
from .models import Donation
from .stripe_utils import create_payment_intent, confirm_payment_intent
from .forms import DonationForm


def create_donation_payment(request):
    """
    Create a Stripe PaymentIntent for donation
    """
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            
            # Create metadata for Stripe
            metadata = {
                'donor_name': donation.donor_name,
                'donor_email': donation.donor_email,
                'donation_type': donation.donation_type,
                'is_anonymous': str(donation.is_anonymous)
            }
            
            # Create payment intent
            result = create_payment_intent(
                amount=donation.amount,
                metadata=metadata
            )
            
            if result['success']:
                # Store payment intent ID temporarily
                request.session['payment_intent_id'] = result['payment_intent_id']
                request.session['donation_data'] = {
                    'donor_name': donation.donor_name,
                    'donor_email': donation.donor_email,
                    'amount': str(donation.amount),
                    'donation_type': donation.donation_type,
                    'message': donation.message,
                    'is_anonymous': donation.is_anonymous
                }
                
                return JsonResponse({
                    'success': True,
                    'client_secret': result['client_secret']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result['error']
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhook events
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        import stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Get donation data from session or metadata
        donation_data = request.session.get('donation_data')
        if donation_data:
            # Create donation record
            Donation.objects.create(
                donor_name=donation_data['donor_name'],
                donor_email=donation_data['donor_email'],
                amount=donation_data['amount'],
                donation_type=donation_data['donation_type'],
                message=donation_data['message'],
                is_anonymous=donation_data['is_anonymous']
            )
            
            # Clear session data
            if 'donation_data' in request.session:
                del request.session['donation_data']
            if 'payment_intent_id' in request.session:
                del request.session['payment_intent_id']
    
    return JsonResponse({'status': 'success'})
