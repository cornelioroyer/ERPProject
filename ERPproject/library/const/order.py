__author__ = 'FARID ILHAM Al-Q'
from django.conf import settings
ugettext = lambda s: s
SO_STATUS_CHOICES = getattr(settings, 'SO_STATUS_CHOICES', ((1, ugettext('Draf')),
                                                            (2, ugettext('Rekonsiliasi')),
                                                            (3, ugettext('Setuju')),
                                                            (4, ugettext('Batal'))))


SO_FINISH_STATUS = getattr(settings, 'SO_FINISH_STATUS', [3])

PAYMENT_TYPE = getattr(settings, 'PAYMENT_TYPE', ((1, ugettext('Tunai')), (2, ugettext('Kredit'))))

SALES_TYPE = getattr(settings, 'SALES_TYPE',  ((1, ugettext('Penjualan Lokal')), (2, ugettext('Penjualan Ekspor'))))

INVOICE_STATUS_CHOICES = getattr(settings, 'INVOICE_STATUS_CHOICES', ((1, ugettext('Draf')),
                                                                      (2, ugettext('Validasi')),
                                                                      (3, ugettext('Pengingat')),
                                                                      (4, ugettext('Lunas'))))

INVOICE_FINISH_STATUS = getattr(settings, 'INVOICE_FINISH_STATUS', (2, 3, 4))

DELIVERY_STATUS_CHOICES = getattr(settings, 'DELIVERY_STATUS_CHOICES', ((1, ugettext('Pending')),
                                                                        (2, ugettext('Progress')),
                                                                        (3, ugettext('Delivered'))))
DO_FINISH_STATUS = getattr(settings, 'DELIVERY_STATUS_CHOICES', (3, ugettext('Delivered')))
YEAR_STATUS = getattr(settings, 'YEAR_STATUS', ((1, ugettext('Buka Tahun')),
                                                (2, ugettext('Tutup Tahun'))))

READONLY_FISCAL = getattr(settings, 'READONLY_FISCAL', [2])

PERIOD_STATUS = getattr(settings, 'PERIOD_STATUS', ((1, ugettext('Buka Periode')),
                                                    (2, ugettext('Tutup Periode'))))

READONLY_PERIOD = getattr(settings, 'READONLY_PERIOD', [2])
