"""
plugin_name: stripe
plugin_type: PAYMENT_PROCESSOR
plugin_uri: https://github.com/nxtbn-com/stripe
version: 1.0.1
author: bytenyx limited
author_uri: http://bytenyx.com
description: plugin to handle payment via stripe.
license: BSD-3-Clause
nxtbn_version_compatibility: >=1.0.0
"""

from nxtbn.payment.plugins.stripe.stripe_gateway import StripePaymentGateway

gateway = StripePaymentGateway

__all__ = ['gateway']
