import types
from django.contrib import auth
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

from .models import Key


ACTIONS = {
    ADDITION: 'Addition',
    CHANGE: 'Change',
    DELETION: 'Deletion',
}


def make_logger(key):
    def logger(self, obj, action_flag=CHANGE, notes=None):
        # self = request

        if notes is None:
            notes = unicode(obj)

        LogEntry.objects.log_action(
            user_id = self.user.pk,
            content_type_id = ContentType.objects.get_for_model(obj).pk,
            object_id = obj.pk,
            object_repr = notes,
            action_flag = action_flag
        )

        if key:
            key.log(
                action = ACTIONS[action_flag] if action_flag in ACTIONS else 'Unknown',
                content_object = obj,
                notes = notes,
            )

    logger.ADDITION = ADDITION
    logger.CHANGE = CHANGE
    logger.DELETION = DELETION

    return logger

class ValetKeyMiddleware(object):
    def process_request(self, request):
        key = None

        if request.META.has_key('HTTP_AUTHORIZATION'):
            authentication = request.META['HTTP_AUTHORIZATION']
            method, credentials = authentication.split(' ', 1)

            if 'basic' == method.lower():
                credentials = credentials.strip().decode('base64')
                key_id, secret = credentials.split(':', 1)

                try:
                    key = Key.objects.get(key=key_id)
                    if key.check_secret(secret):
                        request.user = key.user
                except Key.DoesNotExist:
                    pass

        request.log_action = types.MethodType(make_logger(key), request, request.__class__)
