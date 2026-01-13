from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.payment_profile, name='payment_profile'),
    path('upload-proof/<int:auction_id>/', views.upload_payment_proof, name='upload_payment_proof'),
    path('confirm-payment/<int:payment_proof_id>/', views.confirm_payment_received, name='confirm_payment_received'),
    path('history/', views.payment_history, name='payment_history'),
    path('platform-details/', views.platform_payment_details, name='platform_payment_details'),
    path("invoice/<int:auction_id>/", views.invoice_view, name="invoice_view"),
    path("pay/<int:invoice_id>/", views.pay_invoice, name="pay_invoice"),
] 
