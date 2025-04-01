from django.contrib import admin
from .models import Vocab

@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    list_display = ('word', 'category', 'status', 'meaning', 'example', 'formatted_created_at')

    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%b %d')
    formatted_created_at.admin_order_field = 'created_at'
    formatted_created_at.short_description = 'Created At'
    list_filter = ('status', 'category')
    # search_fields = ('word', 'meaning', 'example')
    fieldsets = (
        (None, {
            'fields': ('word', 'meaning', 'example')
        }),
        (None, {
            'fields': ('status', 'category')
        }),
    )

