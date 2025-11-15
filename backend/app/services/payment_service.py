"""
Jukeyman Autonomous Media Station (JAMS) - Payment Service (Stripe)
"""
import stripe
import logging
from typing import Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """
    Service for handling payments via Stripe
    """
    
    @staticmethod
    async def create_checkout_session(
        product_id: str,
        product_name: str,
        amount: float,
        currency: str = "usd",
        success_url: str = None,
        cancel_url: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session
        
        Args:
            product_id: Product ID
            product_name: Product name
            amount: Amount in dollars (will be converted to cents)
            currency: Currency code
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect after cancelled payment
            metadata: Additional metadata
            
        Returns:
            Checkout session info with URL
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': int(amount * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url or f"{settings.APP_NAME}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=cancel_url or f"{settings.APP_NAME}/cancel",
                metadata=metadata or {}
            )
            
            logger.info(f"Created Stripe checkout session: {session.id}")
            
            return {
                'session_id': session.id,
                'url': session.url,
                'amount': amount,
                'currency': currency
            }
        
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise Exception(f"Payment error: {str(e)}")
    
    @staticmethod
    async def verify_webhook(payload: bytes, sig_header: str) -> Dict[str, Any]:
        """
        Verify and parse Stripe webhook
        
        Args:
            payload: Request body
            sig_header: Stripe-Signature header
            
        Returns:
            Event dictionary
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            raise ValueError("Invalid signature")
    
    @staticmethod
    async def create_refund(payment_intent_id: str, amount: int = None) -> Dict[str, Any]:
        """
        Create a refund
        
        Args:
            payment_intent_id: Payment Intent ID
            amount: Amount in cents (None for full refund)
            
        Returns:
            Refund info
        """
        try:
            refund_params = {'payment_intent': payment_intent_id}
            if amount:
                refund_params['amount'] = amount
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Created refund: {refund.id}")
            
            return {
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100
            }
        
        except stripe.error.StripeError as e:
            logger.error(f"Refund error: {e}")
            raise Exception(f"Refund error: {str(e)}")


# Global instance
payment_service = PaymentService()

