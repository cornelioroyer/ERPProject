from django.conf import settings
ugettext = lambda s: s

PENENTUAN_PEMENANG_CHOICES =  getattr(settings, 'PENENTUAN_PEMENANG_CHOICES', (('manual', ugettext('Manual')),
																				('otomatis', ugettext('Otomatis'))))

LEVEL_AKSES_CHOICES =  getattr(settings, 'LEVEL_AKSES_CHOICES', (('pengendali_gudang', ugettext('Pengendali Gudang')),
																('pengendali_financial', ugettext('Pengendali Financial')),
																('pengendali_proc', ugettext('Pengendali Procurement')),
																('rkb_maker', ugettext('RKB Maker')),
																('kasi_impor', ugettext('Kasi Impor')),
																('kasi_lokal', ugettext('Kasi Lokal')),
																('kasi_intern', ugettext('Kasi Internal')),
																('pel_impor', ugettext('Pelaksana Impor')),
																('pel_lokal', ugettext('Pelaksana Lokal')),
																('pel_intern', ugettext('Pelaksana Internal')),
																('asset', ugettext('Asset Staff')),
																('kabag_proc', ugettext('Kabag Procurement'))))

STATUS_TETAP_CHOICES = getattr(settings, 'STATUS_TETAP_CHOICES', (('tenaga_ahli_tetap', ugettext('Tenaga Ahli Tetap')),
																('tenaga_ahli_tidak_tetap', ugettext('Tenaga Ahli Tidak Tetap'))))

STATUS_ALAT_CHOICES =  getattr(settings, 'STATUS_ALAT_CHOICES', (('siap', ugettext('Siap')),
																('diperbaiki', ugettext('Diperbaiki')),
																('dipinjam', ugettext('Dipinjam'))))
DROP_DOWN_CHOICES = getattr(settings, 'DROP_DOWN_CHOICES', (('1', ugettext('1')),
																('2', ugettext('2')),
																('3', ugettext('3')),
																('4', ugettext('4')),
																('6', ugettext('6')),
																('12', ugettext('12'))))

PO_STATUS_CHOICES = getattr(settings, 'PO_STATUS_CHOICES', ((1, ugettext('Draft')),
																(21, ugettext('Sent')),
																(22, ugettext('Receipt')),
																(23, ugettext('Closed'))))

BR_STATUS_CHOICES = getattr(settings, 'BR_STATUS_CHOICES', ((1, ugettext('Draft')),
																(2, ugettext('Sent'))))

RO_STATUS_CHOICES = getattr(settings, 'RO_STATUS_CHOICES', ((1, ugettext('Rush Order')),
																(2, ugettext('Asset Order'))))

PP_STATE_CHOICES = getattr(settings, 'PP_STATE_CHOICES', ((1, ugettext('Lokal')),
																(2, ugettext('Impor')),
																(3, ugettext('Internal'))))

PP_METHOD_CHOICES = getattr(settings, 'PP_METHOD_CHOICES', ((1, ugettext('Public Tender')),
																(2, ugettext('Direct Appointment')),
																(3, ugettext('Direct Order'))))

YEAR_STATUS = getattr(settings, 'YEAR_STATUS', ((1, ugettext('Tahun Berjalan')),
												(2, ugettext('Tutup Tahun'))))

GRADE_CHOICES = getattr(settings, 'GRADE_CHOICES', ((1, ugettext('A Sangat Memuaskan')),
																(2, ugettext('B Memuaskan')),
																(3, ugettext('C Cukup Memuaskan')),
																(4, ugettext('D Kurang Memuaskan')),
																(5, ugettext('E Tidak Memuaskan'))))

LATE_DAYS_CHOICES = getattr(settings, 'LATE_DAYS_CHOICES', ((1, ugettext('every days')),
																(2, ugettext('every 2 days')),
																(3, ugettext('every 5 days')),
																(4, ugettext('every 7 days')),
																(5, ugettext('every 10 days')),
																(6, ugettext('every 15 days')),
																(7, ugettext('every month'))))

RKB_REG_PREFIX =  getattr(settings, 'RKB_REG_PREFIX', "RKB")
