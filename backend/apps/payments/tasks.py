from celery import shared_task
from django.core.mail import EmailMessage
from .services.invoice import render_invoice_pdf
from .models import Payment

@shared_task
def send_payment_receipt(payment_id):
    payment = Payment.objects.get(pk=payment_id)
    pdf = render_invoice_pdf(payment)
    email = EmailMessage(
        subject="Your OneGo Payment Receipt",
        body="Thank you for your purchase. Please find attached invoice.",
        to=[payment.user.email]
    )
    email.attach(f"invoice_{payment.pk}.pdf", pdf, "application/pdf")
    email.send()
