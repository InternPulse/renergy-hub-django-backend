from django.apps import AppConfig
        
    
class FinancialAnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financial_analytics'

    def ready(self):
        import financial_analytics.signals

