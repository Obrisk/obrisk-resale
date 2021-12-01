from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from obrisk.utils.context_processors import oss
from obrisk.classifieds.models import (
        Classified, ClassifiedImages,
        ClassifiedTags, ClassifiedOrder
    )


oss = oss + "/"

def classified_action(modeladmin, request, queryset):
    for classified in queryset:
        classified.status = "E"
        classified.save()

classified_action.short_description = 'Set Expired'


def img_attach_action(modeladmin, request, queryset):

    selected = queryset.values_list('pk', flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect(
        '/i/wsguatpotlfwccdi/admin-attach-img/?ct=%s&ids=%s' % (
            ct.pk,
            ','.join(str(pk) for pk in selected),
        )
    )

img_attach_action.short_description = 'Attach to Classified'


admin.site.register(ClassifiedTags)
admin.site.register(ClassifiedOrder)

@admin.register(Classified)
class ClassifiedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')
    list_filter = ('status', 'timestamp', 'city')
    search_fields = ['title', 'details', 'english_address']
    actions = [classified_action,]


@admin.register(ClassifiedImages)
class ClassifiedAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(
                    f'<img src="{oss+obj.image_thumb}" style="width: 105px; height:105px;" />'
                )
        else:
            return 'No Image Found'


    list_display = ('image_tag', 'classified', 'wx_classified')
    list_filter = ('classified',)
    actions = [img_attach_action,]
