from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model

from pwa_webpush.utils import send_notification_to_user


def paginate_data(qs, page_size, page, paginated_type, **kwargs):
    """Helper function to turn many querysets
    into paginated results at
    dispose of our GraphQL API endpoint."""
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)

    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def ajax_required(f):
    """Not a mixin, but a nice decorator
    to validate that a request is AJAX"""
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class AdminRequiredMixin(View):
    """Mixin to validate that
    the loggedin user is the creator of the object
    to be edited or updated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AuthorRequiredMixin(View):
    """Mixin to validate that
    the loggedin user is the creator of the object
    to be edited or updated."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class OfficialUserRequiredMixin(View):
    """Mixin to validate that
    the loggedin user is the creator of the object
    to be edited or updated."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user.is_official is False:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


def send_push_notif(recipient_id, title, body, notif_type='Message'):
    try:
        user = get_object_or_404(get_user_model(), pk=recipient_id)

        url = "https://www.obrisk.com/"
        if user and notif_type == 'Message':
            url =  "https://www.obrisk.com/ws/messages/"

        payload = {
            'head': title,
            'body': body,
            'icon': 'https://obrisk.oss-cn-hangzhou.aliyuncs.com/static/img_obj/favicon.png',
            'url': url
        }
        send_notification_to_user(user=user, payload=payload, ttl=1000)
        return {"status": "200", "message": "Web push successful"}

    except TypeError:
        return {"status": "500", "message": "Web push failed"}


def redirect_browser(request):
    """This function is here for reference
    it is never called by any urls in obrisk.
    It was pushing the user out of wechat browser for android users."""
    if request.user_agent.browser.family == 'Mobile Safari':
        return redirect('ios_download', permanent=True)
    else:
        response = HttpResponseRedirect('/classifieds/')
        response['Content-Disposition'] = 'attachment;filename=open.pdf'
        response['Content-Type'] = 'text/plain; charset=utf-8'
        response['If-None-Match'] = None
        response['If-Modified-Since'] = None
        response.status_code = 206
        return response
