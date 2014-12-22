''' @author: Fery Febriyan Syah '''

from django.conf import settings
from django.utils.translation import ugettext
from webbrowser import get
ugettext = lambda s: s


GENDER = getattr (settings, 'GENDER',  ((1, ugettext ('Laki - Laki')),
                                        (2, ugettext ('Perempuan'))))
                                       
           
RELIGION = getattr (settings, 'RELIGION', ((1, ugettext ('Islam')),
                                           (2, ugettext ('Protestan')),
                                           (3, ugettext ('Katolik')),
                                           (4, ugettext ('Hindu')),
                                           (5, ugettext ('Budha'))))
                                          


STATUS = getattr (settings, 'STATUS', ((1, ugettext ('Belum Menikah')),
                                       (2, ugettext ('Menikah')),
                                       (3, ugettext ('Janda')),
                                       (4, ugettext ('Duda'))))


STATUS2 = getattr (settings, 'STATUS2', ((1, ugettext ('Draf')),
                                         (2, ugettext ('Rekonsiliasi')),
                                         (3, ugettext ('Setuju')),
                                         (4, ugettext ('Batal'))))


STATUS_EMPLOYEE = getattr( settings, 'STATUS_EMPLOYEE', ((1, ugettext ('Aktif')),
                                                         (2, ugettext ('Pensiun'))))


EDU_STATUS = getattr (settings, 'EDU_STATUS', ((1, ugettext ('SD')),
                                               (2, ugettext ('SMP')),
                                               (3, ugettext ('SMK')),
                                               (4, ugettext ('SMA')),
                                               (5, ugettext ('S1')),
                                               (6, ugettext ('S2')),
                                               (7, ugettext ('S3'))))


BLOOD = getattr (settings, 'BLOOD', ((1, ugettext ('A')),
                                     (2, ugettext ('B')),
                                     (3, ugettext ('O')),
                                     (4, ugettext ('AB'))))


NATIONAL = getattr (settings, 'NATIONAL', ((1, ugettext ('WNI')),
                                           (2, ugettext ('WNA'))))


HOUSE = getattr (settings, 'HOUSE', ((1, ugettext ('Rumah Kontrakan')),
                                     (2, ugettext ('Rumah Kost')),
                                     (3, ugettext ('Rumah Orang Tua')),
                                     (4, ugettext ('Rumah Pribadi'))))


LEAVE = getattr (settings, 'LEAVE', ((1, ugettext ('Cuti Tahunan')),
                                     (2, ugettext ('Cuti Besar')),
                                     (3, ugettext ('Cuti Sakit')),
                                     (4, ugettext ('Cuti Bersalin')),
                                     (5, ugettext ('Cuti Alasan Penting')),
                                     (6, ugettext ('Cuti Sekolah'))))


HOBBY = getattr (settings, 'HOBBY', ((1, ugettext ('Filateli')),
                                     (2, ugettext ('Fotografi')),
                                     (3, ugettext ('Kaligrafi')),
                                     (4, ugettext ('Menulis')),
                                     (5, ugettext ('Origami')),
                                     (6, ugettext ('Otomotif')),
                                     (7, ugettext ('Olahraga')),
                                     (8, ugettext ('Nyanyi'))))


SANKSI = getattr( settings, 'SANKSI', ((1, ugettext ('Sangsi Ringan')),
                                       (2, ugettext ('Sangsi Sedang')),
                                       (3, ugettext ('Sangsi Berat'))))


TASK = getattr( settings, 'TASK', ((1, ugettext ('Tugas Luar Kota')),
                                   (2, ugettext ('Tugas Dalam Kota')),
                                   (3, ugettext ('Tugas Luar Negeri'))))


TERMINATION = getattr (settings, 'TERMINATION', ((1, ugettext('Pemecatan')),
                                                 (2, ugettext ('Pengunduran Diri')),
                                                 (3, ugettext ('PHK'))))


SEMINAR = getattr( settings, 'SEMINAR', ((1, ugettext ('Seminar Nasional')),
                                         (2, ugettext ('Seminar Internasional'))))


RESULT1 = getattr (settings, 'RESULT1', ((1, ugettext ('Lulus')),
                                         (2, ugettext ('Tidak Lulus'))))


RESULT2 = getattr (settings, 'RESULT2', ((1, ugettext ('Diterima')),
                                         (2, ugettext ('Tidak Diterma')),
                                         (3, ugettext ('Cadangan'))))


CHECK = getattr (settings, 'CHECK', ((1, ugettext('Ada')),
                                     (2, ugettext ('Tidak Ada'))))


LEVEL_AKSES =  getattr(settings, 'LEVEL_AKSES', (('Direktur', ugettext('Direktur')),
                                                 ('Kadep', ugettext('Kepala Departemen ')),
                                                 ('Kabag', ugettext('Kepala Bagian')),
                                                 ('Admin', ugettext('Admin SDM'))))


STATUS_PEGAWAI = getattr(settings, 'STATUS_PEGAWAI', ((1, ugettext('Pegawai Tetap')),
                                                      (2, ugettext('Buruh'))))


SHIFT = getattr(settings, 'SHIFT', ((1, ugettext('Shift Pagi')),
                                    (2, ugettext ('Shift Malam'))))
                
