from django.contrib import admin
from django.utils.safestring import mark_safe

from obrisk.classifieds.models import (
        Classified, ClassifiedImages,
        ClassifiedTags, ClassifiedOrder
    )


def classified_action(modeladmin, request, queryset):
    for classified in queryset:
        classified.status = "E"
        classified.save()

classified_action.short_description = 'Set Expired'


admin.site.register(ClassifiedTags)
admin.site.register(ClassifiedOrder)

@admin.register(Classified)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('status', 'timestamp', 'city')
    search_fields = ['title', 'user', 'details', 'address']
    actions = [classified_action,]


@admin.register(ClassifiedImages)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('classified', 'wx_classified')
    list_filter = ('classified',)
