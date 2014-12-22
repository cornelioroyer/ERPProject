''' @author: Fery Febriyan Syah '''

from django.conf import settings
ugettext = lambda s: s
from django.utils.translation import ugettext

MONTH = getattr (settings, 'MONTH', ((1, ugettext ('Januari')),
                                     (2, ugettext ('Februari')),
                                     (3, ugettext ('Maret')),
                                     (4, ugettext ('April')),
                                     (5, ugettext ('Mei')),
                                     (6, ugettext ('Juni')),
                                     (7, ugettext ('Juli')),
                                     (8, ugettext ('Agustus')),
                                     (9, ugettext ('September')),
                                     (10, ugettext ('Oktober')),
                                     (11, ugettext ('Nopember')),
                                     (12, ugettext ('Desember'))))

