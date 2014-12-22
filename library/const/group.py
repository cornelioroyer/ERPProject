''' @author: Fery Febriyan Syah '''

from django.conf import settings
ugettext = lambda s: s
from django.utils.translation import ugettext


GROUP = getattr (settings, 'GROUP', ((1, ugettext ('1A')),
                                     (2, ugettext ('1B')),
                                     (3, ugettext ('1C')),
                                     (4, ugettext ('1D')),
                                     (5, ugettext ('2A')),
                                     (6, ugettext ('2B')),
                                     (7, ugettext ('2C')),
                                     (8, ugettext ('2D')),
                                     (9, ugettext ('3A')),
                                     (10, ugettext ('3B')),
                                     (11, ugettext ('3C')),
                                     (12, ugettext ('3D')),
                                     (13, ugettext ('4A')),
                                     (14, ugettext ('4B')),
                                     (15, ugettext ('4C')),
                                     (16, ugettext ('4D')),
                                     (17, ugettext ('5A')),
                                     (18, ugettext ('5B')),
                                     (19, ugettext ('5C')),
                                     (20, ugettext ('5D')),
                                     (21, ugettext ('6A')),
                                     (22, ugettext ('6B')),
                                     (23, ugettext ('6C')),
                                     (24, ugettext ('6D')),
                                     (25, ugettext ('7A')),
                                     (26, ugettext ('7B')),
                                     (27, ugettext ('7C')),
                                     (28, ugettext ('7D')),
                                     (29, ugettext ('8A')),
                                     (30, ugettext ('8B')),
                                     (31, ugettext ('8C')),
                                     (32, ugettext ('8D')),
                                     (33, ugettext ('9A')),
                                     (34, ugettext ('9B')),
                                     (35, ugettext ('9C')),
                                     (36, ugettext ('9D'))))
