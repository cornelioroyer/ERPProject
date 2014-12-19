from django.conf import settings
ugettext = lambda s: s

tipe_maintenance = getattr(settings,'tipe_maintenance',((1, ugettext('Repair A')),
															(2, ugettext('Repair B')),
															(3, ugettext('Repair C'))))
															
status_maintenance = getattr(settings,'status_maintenance',((1, ugettext('None')),
															(2, ugettext('Dalam Perbaikan'))))

Pilihan_request = getattr(settings,'Pilihan_request',((1, ugettext('Pengadaan')),
														(2, ugettext('Perbaikan')),
														(3, ugettext('Peminjaman'))))

status_ganti= getattr(settings,'status_ganti',((1, ugettext('None')),
														(2, ugettext('Diganti'))))
														
Usage_choice = getattr(settings,'Usage_choice',((1, ugettext('Masih Digunakan')),
														(2, ugettext('Tidak Digunakan'))))
														
														
metode_pembayaran = getattr(settings,'metode_pembayaran',((1, ugettext('Tunai')),
																(2, ugettext('Kredit'))))	

metode_penjualan = getattr(settings,'metode_penjualan',((1, ugettext('Penjualan Langsung')),
																(2, ugettext('Pelelangan'))))
														
Pilihan_service = getattr(settings,'Pilihan_service',((11, ugettext('Pengadaan')),
														(2, ugettext('Perbaikan')),
														(13, ugettext('Penggantian')),
														(4, ugettext('Pemindahan')),
														(5, ugettext('Peminjaman')),
														(6, ugettext('Penghapusan')),
														(7, ugettext('Ditolak'))))

LEVEL_AKSES_CHOICES =  getattr(settings, 'LEVEL_AKSES_CHOICES', (('staff', ugettext('Asset Staff')),
																	('unit', ugettext('Unit Kerja')),
																	('manager', ugettext('Manager'))))

Tipe_vendor = getattr(settings,'Tipe_vendor',((1, ugettext('Gedung')),
												(2, ugettext('Mesin')),
												(3, ugettext('Tanah')),
												(4, ugettext('Lain-Lain'))))	
	
Choice_month_report = getattr(settings,'Choice_month_report',((1, ugettext('1 Bulan')),
																(2, ugettext('3 Bulan')),
																(3, ugettext('1 tahun'))))

Choice_peminjaman = getattr(settings,'Choice_peminjaman',((1, ugettext('None')),
																(2, ugettext('Dipinjamkan'))))
																
Status_penghapusan = getattr(settings,'Status_penghapusan',((1, ugettext('Akan Segera Dihapus')),
																(2, ugettext('Sudah Dihapus')))) 	

per_choices = getattr(settings,'per_choices',((1, ugettext('per Hari')),
												(2, ugettext('per Minggu')),
												(3, ugettext('per 2 Minggu')),
												(4, ugettext('per Bulan')),
												(5, ugettext('per Semester')),
												(6, ugettext('per Tahun')))) 																	

Freq_pemeliharaan = getattr(settings,'Freq_pemeliharaan',((1, ugettext('1 bulan ')),
															(3, ugettext('3 bulan ')),
															(6, ugettext('6 bulan')))) 

Choice_kondisi = getattr(settings,'Choice_kondisi',((1, ugettext('Baru')),
																(2, ugettext('Bekas')))) 

DROP_DOWN_CHOICES = getattr(settings, 'DROP_DOWN_CHOICES', (('1', ugettext('1')),
																('2', ugettext('2')),
																('3', ugettext('3')),
																('4', ugettext('4')),
																('6', ugettext('6')),
																('12', ugettext('12'))))																