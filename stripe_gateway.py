import stripe
from decimal import Decimal
from django.conf import settings
from nxtbn.payment.base_payment_gateway import BasePaymentGateway, PaymentResponse
from rest_framework import serializers

from nxtbn.settings import get_env_var

stripe.api_key = get_env_var('STRIPE_SECRET_KEY', '')

class StripePayloadSerializer(serializers.Serializer):
    stripe_payment_method_id = serializers.CharField(max_length=500, required=True)

class StripePaymentGateway(BasePaymentGateway):
    """Stripe payment gateway implementation."""

    gateway_name = 'stripe'
    
    def authorize(self, amount: Decimal, order_id: str, **kwargs):
        """Authorize a payment with Stripe."""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100), 
                currency='usd',
                payment_method=kwargs.get("payment_method_id"),
                confirmation_method='manual',  # authorize but don't capture
                confirm=True,
                metadata={'order_id': order_id},
            )
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def capture(self, amount: Decimal, order_id: str, **kwargs):
        """Capture a previously authorized payment."""
        payment_intent_id = kwargs.get("payment_intent_id")
        try:
            # Capture the authorized payment
            intent = stripe.PaymentIntent.capture(payment_intent_id)
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def cancel(self, order_id: str, **kwargs):
        """Cancel an authorized payment."""
        payment_intent_id = kwargs.get("payment_intent_id")
        try:
            # Cancel the authorized payment
            intent = stripe.PaymentIntent.cancel(payment_intent_id)
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def refund(self, amount: Decimal, order_id: str, **kwargs):
        """Refund a captured payment."""
        charge_id = kwargs.get("charge_id")
        try:
            # Create a refund for the charge
            refund = stripe.Refund.create(
                charge=charge_id,
                amount=int(amount * 100),  # Stripe expects the amount in cents
            )
            return self.normalize_response(refund)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def normalize_response(self, raw_response):
        """Normalize the Stripe response to a consistent PaymentResponse."""
        return PaymentResponse(
            success=raw_response.get("status") in ["succeeded", "canceled", "refunded"],
            transaction_id=raw_response.get("id"),
            message=raw_response.get("status"),
            raw_data=raw_response,
        )

    def special_serializer(self):
        """This method will handle payload from client size will be used in api views"""
        return StripePayloadSerializer()
    
    def public_keys(self):
        """
            Retrieve public keys and non-sensitive information required for secure communication and client-side operations with Stripe.

            Returns:
                dict: A dictionary containing public keys and non-sensitive data necessary for client-side operations with Stripe.
                
                Example:
                    {
                        'stripe_public_key': 'your_stripe_public_key',
                        # Add more relevant key-value pairs as needed...
                    }

            This method is intended to provide essential information such as the Stripe public key required for secure communication between the client and the Stripe payment gateway. 
            It's crucial to include only non-sensitive data in the returned dictionary, ensuring the security of client-side operations. 
            Sensitive information such as secret keys should never be included here to maintain security.
        """
        keys = {
            'STRIPE_PUBLIC_KEY': get_env_var('STRIPE_PUBLIC_KEY', '')
        }
        return keys
