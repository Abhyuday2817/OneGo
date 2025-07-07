from django.contrib import admin, messages
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gig_request",
        "gig_title",
        "mentor_username",
        "proposed_rate",
        "status",
        "created_at"
    )
    list_filter = (
        "status",
        "mentor__user__username",
        "gig_request__status",
        "created_at"
    )
    search_fields = (
        "proposal_text",
        "mentor__user__username",
        "gig_request__title"
    )
    actions = ["accept_bids", "reject_bids", "cancel_bids"]

    def gig_title(self, obj):
        return obj.gig_request.title
    gig_title.short_description = "Gig Title"

    def mentor_username(self, obj):
        return obj.mentor.user.username
    mentor_username.short_description = "Mentor"

    def accept_bids(self, request, queryset):
        count = 0
        for bid in queryset:
            if request.user == bid.gig_request.student:
                bid.accept()
                count += 1
        if count:
            self.message_user(request, f"{count} bid(s) accepted.", level=messages.SUCCESS)
        else:
            self.message_user(request, "No bids were accepted (not authorized or already accepted).", level=messages.WARNING)
    accept_bids.short_description = "✅ Accept selected bids"

    def reject_bids(self, request, queryset):
        count = 0
        for bid in queryset:
            if request.user == bid.gig_request.student:
                bid.reject()
                count += 1
        if count:
            self.message_user(request, f"{count} bid(s) rejected.", level=messages.SUCCESS)
        else:
            self.message_user(request, "No bids were rejected (not authorized or already rejected).", level=messages.WARNING)
    reject_bids.short_description = "❌ Reject selected bids"

    def cancel_bids(self, request, queryset):
        count = 0
        for bid in queryset:
            if request.user == bid.mentor.user and bid.status == Bid.STATUS_PENDING:
                bid.cancel()
                count += 1
        if count:
            self.message_user(request, f"{count} bid(s) cancelled by mentor.", level=messages.SUCCESS)
        else:
            self.message_user(request, "No bids were cancelled (not authorized or already resolved).", level=messages.WARNING)
    cancel_bids.short_description = "🗑️ Cancel selected bids (Mentor only)"
