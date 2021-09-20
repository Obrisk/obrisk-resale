from django.contrib import admin
from obrisk.messager.models import Message, WechatMessage, Conversation

admin.site.register(Conversation)
admin.site.register(WechatMessage)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp", "message","classified", "image")
    list_filter = ("sender", "recipient")
