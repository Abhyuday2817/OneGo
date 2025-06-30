import io
from reportlab.pdfgen import canvas
from django.utils.timezone import localtime

def render_invoice_pdf(payment):
    buf = io.BytesIO()
    p = canvas.Canvas(buf)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50,800,"OneGo Invoice")
    p.setFont("Helvetica",12)
    p.drawString(50,770,f"Invoice #: PAY-{payment.pk:06d}")
    p.drawString(50,750,f"Date: {localtime(payment.created_at).strftime('%Y-%m-%d')}")
    p.drawString(50,730,f"User: {payment.user.username}")
    p.drawString(50,710,f"Amount: {payment.amount:.2f} {payment.currency}")
    p.drawString(50,690,f"Status: {payment.status}")
    p.drawString(50,670,"Thank you for your payment!")
    p.showPage()
    p.save()
    buf.seek(0)
    return buf.read()
