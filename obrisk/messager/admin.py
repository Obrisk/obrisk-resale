from django.contrib import admin
from obrisk.messager.models import Message, Conversation

admin.site.register(Conversation)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp")
    list_filter = ("sender", "recipient")
