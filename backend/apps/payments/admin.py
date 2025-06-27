
# apps/payments/admin.py
from django.contrib import admin
from .models import Wallet, Transaction, Payment
import csv
from django.http import HttpResponse

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "escrowed")
    search_fields = ("user__username",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "txn_type", "amount", "reference", "timestamp")
    list_filter = ("txn_type", "timestamp")
    search_fields = ("user__username", "reference")

    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = "attachment; filename=transactions.csv"
        writer = csv.writer(resp)
        writer.writerow(["User", "Type", "Amount", "Ref", "When"])
        for t in queryset:
            writer.writerow([t.user.username, t.txn_type, t.amount, t.reference, t.timestamp])
        return resp
    export_csv.short_description = "Export selected to CSV"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "created_at")  # Removed 'currency'
    list_filter = ("status", "created_at")  # Removed 'currency'
    search_fields = ("user__username", "transaction_id")
    readonly_fields = ("created_at", "updated_at")
