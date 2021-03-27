from django.contrib import admin
from obrisk.classifieds.models import (
        Classified, ClassifiedImages,
        ClassifiedTags, ClassifiedOrder
    )


admin.site.register(ClassifiedImages)
admin.site.register(ClassifiedTags)
admin.site.register(ClassifiedOrder)

@admin.register(Classified)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('user', 'status', 'timestamp')
