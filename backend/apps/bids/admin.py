from django.contrib import admin
from .models import Bid

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display  = ("id", "gig_request", "mentor", "proposed_rate", "status", "created_at")
    list_filter   = ("status", "mentor__user__username", "gig_request__status")
    search_fields = ("proposal_text", "mentor__user__username", "gig_request__title")
    actions       = ["accept_bids", "reject_bids"]

    def accept_bids(self, request, queryset):
        student = request.user
        for bid in queryset:
            if bid.gig_request.student == student:
                bid.accept()
        self.message_user(request, "Selected bids accepted.")
    accept_bids.short_description = "Accept selected bids"

    def reject_bids(self, request, queryset):
        student = request.user
        for bid in queryset:
            if bid.gig_request.student == student:
                bid.reject()
        self.message_user(request, "Selected bids rejected.")
    reject_bids.short_description = "Reject selected bids"
