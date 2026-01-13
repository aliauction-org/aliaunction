from django.apps import AppConfig

class BidProtectionConfig(AppConfig):
    name = 'bid_protection'

    def ready(self):
        import bid_protection.signals
