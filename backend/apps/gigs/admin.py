from django.contrib import admin
from .models import GigRequest, Bid, Contract

class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ("mentor", "proposed_rate", "status", "created_at")

class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0
    readonly_fields = ("bid", "student", "mentor", "status", "start_date", "end_date")

@admin.register(GigRequest)
class GigRequestAdmin(admin.ModelAdmin):
    list_display   = ("id", "title", "student", "status", "bidding_deadline", "created_at")
    list_filter    = ("status", "category")
    search_fields  = ("title", "description", "student__username")
    inlines        = [BidInline, ContractInline]

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display  = ("id", "gig_request", "mentor", "proposed_rate", "status", "created_at")
    list_filter   = ("status",)
    search_fields = ("gig_request__title", "mentor__user__username")

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display  = ("id", "gig_request", "mentor", "student", "status", "start_date", "end_date")
    list_filter   = ("status",)
    search_fields = ("bid__gig_request__title", "mentor__user__username", "student__username")
