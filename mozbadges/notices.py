try:

    from notification.models import send, send_now, queue, observe, stop_observing, is_observing

except ImportError:

    def send(*args, **kwargs):
        return False

    def send_now(*args, **kwargs):
        return False

    def queue(*args, **kwargs):
        return False

    def observe(*args, **kwargs):
        return False

    def stop_observing(*args, **kwargs):
        return False

    def is_observing(*args, **kwargs):
        return False
