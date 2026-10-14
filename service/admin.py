from django.contrib import admin
from .models import Category, Ticket, Comment

# Register your models here.


admin.site.register(Category)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_by',
        'assigned_to',
        'category',
        'priority',
        'status',
        'created_at',
    )
    search_fields = ('title', 'description')

    list_filter = ('priority', 'status', 'category')

    fields = (
    'created_by',
    'assigned_to',
    'title',
    'description',
    'resolution',
    'category',
    'priority',
    'status',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'user',
        'content',
        'created_at',
    )