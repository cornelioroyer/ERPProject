__author__ = 'FARID ILHAM Al-Q'

from django.utils.translation import ugettext_lazy as _

TYPE_BISNIS = (
    ('1',_('Perseroan Terbatas (PT)')),
    ('2',_('Perseroan Komanditer (CV)')),
    ('3',_('Firma (Fa)')),
    ('4',_('Others')),
)

BISNIS = (
    ('1', _('Manufacturer')),
    ('2', _('Identer')),
    ('3', _('Trader / Distributor')),
    ('4', _('Others'))
)

REGION = (
    ('1', _('Domestik')),
    ('2', _('Luar Negeri'))
)

INDUSTRI = (
    ('1', _('Beverages')),
    ('2', _('Pharmaceuticals')),
    ('3', _('Food & Jars')),
    ('4', _('Breweries')),
    ('5', _('Cosmetic')),
    ('6', _('Others'))
)
