import os
import uuid
import logging
import time
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from celery import shared_task
from obrisk.users.phone_verification import send_sms
from obrisk.classifieds.models import Classified, ClassifiedTags, ClassifiedOrder
from obrisk.messager.send_wxtemplate import notify_seller_wxtemplate


TAGS_TIMEOUT = getattr(
        settings,
        'TAGS_CACHE_TIMEOUT',
        DEFAULT_TIMEOUT
    )

def set_popular_tags():
    popular_tags = Classified.objects.get_active(
            ).get_counted_tags()[:10]

    cache.set('popular_tags_mb',
                list(popular_tags), timeout=TAGS_TIMEOUT
            )

    return HttpResponse(
            "Successfully sorted the popular tags!",
            content_type='text/plain')



@shared_task
def migrate_classifieds_tags():
    '''this function is to update the
    old tags in taggit to new ones in classfieds app'''

    classifieds = Classified.objects.all()
    for classified in classifieds:
        tags = classified.tags.all()
        for tag in tags:
            classified.new_tags.add(str(tag))
        classified.save()


@shared_task
def update_classified_tags():
    set_popular_tags()


@shared_task
def add_tags(item_id):
    time.sleep(5)
    classified = Classified.objects.get(id=item_id)
    tags = ClassifiedTags.objects.values_list('slug', flat=True)

    for title in classified.title.split():
        if title.lower() in tags:
            classified.tags.add(title)
    for det in classified.details.split():
        if det.lower() in tags:
            classified.tags.add(det)

    classified.save()


@shared_task
def order_notify_seller(order_id):
    time.sleep(5)
    order = ClassifiedOrder.objects.get(pk=order_id)

    if order.classified.user.wechat_openid is not None:
        try:
            logging.error(f'Dispatching notify seller task {order}')
            notify_seller_wxtemplate(order)
        except Exception as e:
            logging.error(
                f'Failed to notify seller on Classified Order',
                exc_info=e
            )

    params = " {\"item\":\""+ order.classified.title + "\"} "
    __business_id = uuid.uuid1()

    ret = send_sms(
        __business_id,
        order.classified.user.phone_number.national_number,
        os.getenv('SMS_SIGNATURE'),
        os.getenv('ALI_ORDER_SMS_TEMPLATE'), params
    )

    ret = ret.decode("utf-8")
    response = ast.literal_eval(ret)

    if response['Code'] != 'OK':
        logging.error(
            f'Failed to notify seller via SMS on Classified Order',
            extra=response
        )
