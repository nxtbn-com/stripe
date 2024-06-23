metadata = {
    "plugin_name": "stripe",
    "plugin_type": "PAYMENT_PROCESSOR",
    "plugin_uri": "https://github.com/nxtbn-com/stripe",
    "version": "1.0.1",
    "author": "bytenyx limited",
    "author_uri": "http://bytenyx.com",
    "description": "Plugin to handle payment via stripe.",
    "license": "BSD-3-Clause",
    "nxtbn_version_compatibility": ">=1.0.0",
    "has_urls": true,
    
}

from . stripe.stripe_gateway import StripePaymentGateway

plugin = StripePaymentGateway

__all__ = ['plugin']
