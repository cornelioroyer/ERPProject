__author__ = 'FARID ILHAM AL-Q'
from django.conf.urls import patterns, url
urlpatterns = patterns('',
                       url(r'product/$', 'Apps.Inventory.product.views.index'),
                       url(r'product_item/(?P<id>.*)/$', 'Apps.Inventory.product.views.item'),
                       url(r'product_item_detail/(?P<id>.*)/$', 'Apps.Inventory.product.views.detail_item'),

                       )
