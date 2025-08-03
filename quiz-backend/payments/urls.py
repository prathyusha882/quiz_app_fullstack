from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment processing
    path('create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('<uuid:payment_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('<uuid:payment_id>/confirm/', views.PaymentConfirmView.as_view(), name='payment-confirm'),
    path('<uuid:payment_id>/refund/', views.PaymentRefundView.as_view(), name='payment-refund'),
    
    # Payment history
    path('history/', views.PaymentHistoryView.as_view(), name='payment-history'),
    
    # Webhooks
    path('webhook/stripe/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('webhook/paypal/', views.PayPalWebhookView.as_view(), name='paypal-webhook'),
] 