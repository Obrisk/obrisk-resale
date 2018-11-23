from django.contrib import admin
from obrisk.classifieds.models import Classified


@admin.register(Classified)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('user', 'status', 'timestamp')
