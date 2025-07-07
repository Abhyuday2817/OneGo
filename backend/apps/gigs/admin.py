from django.contrib import admin
from .models import GigRequest, Bid, Contract


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ("mentor", "proposed_rate", "proposal_text", "status", "created_at")
    show_change_link = True
    ordering = ("-created_at",)


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    readonly_fields = ("bid", "student", "mentor", "status", "start_date", "end_date")
    show_change_link = True
    ordering = ("-start_date",)


@admin.register(GigRequest)
class GigRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "student", "category", "status", "bids_count",
        "bidding_deadline", "created_at", "is_open"
    )
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "student__username")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    inlines = [BidInline, ContractInline]
    autocomplete_fields = ["student", "category"]
    readonly_fields = ("created_at", "updated_at")

    def bids_count(self, obj):
        return obj.bids_from_gigs_app.count()
    bids_count.short_description = "Total Bids"

    def is_open(self, obj):
        return obj.is_open()
    is_open.boolean = True
    is_open.short_description = "Open & Active?"


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id", "gig_request", "mentor", "proposed_rate", "status", "created_at", "short_proposal"
    )
    list_filter = ("status", "created_at")
    search_fields = ("gig_request__title", "mentor__user__username", "proposal_text")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    autocomplete_fields = ["gig_request", "mentor"]
    readonly_fields = ("created_at", "updated_at")

    def short_proposal(self, obj):
        return obj.proposal_text[:40] + "..." if obj.proposal_text else "-"
    short_proposal.short_description = "Proposal Summary"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id", "gig_request", "mentor", "student", "status", "start_date", "end_date", "is_active"
    )
    list_filter = ("status", "start_date", "end_date")
    search_fields = (
        "gig_request__title", "mentor__user__username", "student__username"
    )
    list_editable = ("status",)
    readonly_fields = ("start_date", "end_date", "bid")
    date_hierarchy = "start_date"
    autocomplete_fields = ["gig_request", "mentor", "student", "bid"]

    def is_active(self, obj):
        return obj.status == Contract.STATUS_ACTIVE
    is_active.boolean = True
    is_active.short_description = "Active?"
