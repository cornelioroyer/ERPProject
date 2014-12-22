import sys

from django.core.management.base import BaseCommand

from Plugins.captcha.models import get_safe_now


class Command(BaseCommand):
    help = "Clean up expired captcha hashkeys."

    def handle(self, **options):
        from Plugins.captcha.models import CaptchaStore

        verbose = int(options.get('verbosity'))
        expired_keys = CaptchaStore.objects.filter(expiration__lte=get_safe_now()).count()
        if verbose >= 1:
            print "Currently %d expired hashkeys" % expired_keys
        try:
            CaptchaStore.remove_expired()
        except:
            if verbose >= 1:
                print "Unable to delete expired hashkeys."
            sys.exit(1)
        if verbose >= 1:
            if expired_keys > 0:
                print "%d expired hashkeys removed." % expired_keys
            else:
                print "No keys to remove."
