'''@author: Fery Febriyan Syah'''

from django.conf import settings
ugettext = lambda s: s

PAYMENT_METHOD =  getattr(settings, 'PAYMENT_METHOD', ((1, ugettext('Cash')), 
                                                       (2, ugettext('Bank'))))

PAYMENT_STATUS =  getattr(settings, 'PAYMENT_STATUS', ((1, ugettext('Belum Terbayar')), 
                                                       (2, ugettext('Terbayar')))) 

YEAR_STATUS =  getattr(settings, 'YEAR_STATUS', ((1, ugettext('Tahun Berjalan')),
                                                (2, ugettext('Tutup Tahun'))))

PERIOD_STATUS =  getattr(settings, 'PERIOD_STATUS', ((1, ugettext('Periode Berjalan')),
                                                    (2, ugettext('Tutup Periode'))))

JOURNAL_TYPE =  getattr(settings, 'JOURNAL_TYPE', ((1, ugettext('Sale')),
                                                    (2, ugettext('Purchase')),
                                                    (3, ugettext('Cash')),
                                                    (4, ugettext('Bank')),
                                                    (5, ugettext('General')),
                                                    (6, ugettext('Adjustment'))))