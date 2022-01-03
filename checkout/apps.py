from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """checkout"""
    name = 'checkout'

    def ready(self):
        import checkout.signals
